import sqlite3
import os
import smtplib
from typing import Annotated, TypedDict
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

# ------------------------------------------------------------------
# ENV
# ------------------------------------------------------------------
load_dotenv()

# ------------------------------------------------------------------
# STATE
# ------------------------------------------------------------------
class State(TypedDict):
    messages: Annotated[list, add_messages]

# ------------------------------------------------------------------
# SYSTEM PROMPT (SHORT + POWERFUL)
# ------------------------------------------------------------------
SYSTEM_PROMPT = {
    "role": "system",
    "content": """ You are an expert in converting English questions to SQL query!
    The SQL database has the name EMPLOYEE and has the following columns - NAME, ID, 
    DEPARTMENT \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM EMPLOYEE ;
    \nExample 2 - Tell me all the employees from HR department?, 
    the SQL command will be something like this SELECT * FROM EMPLOYEE WHERE DEPARTMENT="HR" ; 
    The Sql databsase has another table named ATTENDANCE with the following columns - EMP_ID, DATE, 
    WORK_MODE, STATUS, REASON_ABSENCE. EMP_ID is foreign key referencing ID in EMPLOYEE table.
    \n\nFor example,\nExample 3 - How many employees were absent on 1st Jan 2026?, 
    the SQL command will be something like this SELECT COUNT(*) FROM ATTENDANCE WHERE DATE="2026-01-01" AND STATUS="Absent" ;
    \nExample 4 - List the names of employees who worked remotely on 1st Jan 2026?, 
    the SQL command will be something like this SELECT EMPLOYEE.NAME FROM EMPLOYEE JOIN ATTENDANCE ON EMPLOYEE.ID = ATTENDANCE.EMP_ID WHERE ATTENDANCE.DATE="2026-01-01" AND ATTENDANCE.WORK_MODE="Remote" ;
    also the sql code should not have ``` in beginning or end and sql word in output
    """
}

# ------------------------------------------------------------------
# LLM NODE
# ------------------------------------------------------------------
def chatbot(state: State):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0,
        max_output_tokens=300
    ).bind_tools(tools)

    ai_msg = llm.invoke(state["messages"])
    return {"messages": [ai_msg]}

# ------------------------------------------------------------------
# TOOLS
# ------------------------------------------------------------------
@tool
def execute_query(sql_query: str):
    """Execute a SQLite query on attendance database and return results."""
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute(sql_query)
    rows = cursor.fetchall()
    conn.close()
    return rows


@tool
def send_email(recipient_email: str, reason: str):
    """Send an absence notification email."""
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_EMAIL_PASSWORD")

    subject = "Absence Notification"
    body = f"""
Dear HR,

This is to inform you that I will be absent due to the following reason:
{reason}

Regards,
{sender_email}
"""

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        return f"Email successfully sent to {recipient_email}"

    except Exception as e:
        return f"Email failed: {str(e)}"

# ------------------------------------------------------------------
# TOOLS LIST
# ------------------------------------------------------------------
tools = [execute_query, send_email]

# ------------------------------------------------------------------
# GRAPH
# ------------------------------------------------------------------
builder = StateGraph(State)

builder.add_node("chatbot", chatbot)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "chatbot")
builder.add_conditional_edges("chatbot", tools_condition)
builder.add_edge("tools", "chatbot")
builder.add_edge("chatbot", END)

graph = builder.compile()

# ------------------------------------------------------------------
# CHAT LOOP
# ------------------------------------------------------------------
state = None

while True:
    user_input = input("User: ").strip()
    if user_input.lower() in {"exit", "quit"}:
        break

    if state is None:
        state = {
            "messages": [
                SYSTEM_PROMPT,
                {"role": "user", "content": user_input}
            ]
        }
    else:
        state["messages"].append({"role": "user", "content": user_input})

    state = graph.invoke(state)
    last_msg = state["messages"][-1]
    print("response:",last_msg)
    # CLEAN OUTPUT
    if hasattr(last_msg, "content"):
        if isinstance(last_msg.content, list):
            print("Bot:", last_msg.content[0]["text"])
        else:
            print("Bot:", last_msg.content)
    else:
        print("Bot: Unable to respond.")
