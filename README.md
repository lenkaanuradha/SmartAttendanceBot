🧠 SmartAttendanceBot

SmartAttendanceBot is an Agentic AI–powered chatbot that works on a dummy Employee and Attendance database. It allows users to query attendance information in natural language, automatically converts queries into SQL, executes them on a SQLite database, and returns accurate results. The bot can also send email notifications for employee leaves.

🚀 Features

📊 Query employee attendance using natural language
🔄 Automatically converts user queries into SQL
🗄️ Executes SQL on a SQLite3 database
🧑‍💼 Supports Employee & Attendance dummy databases
📅 Get details like:
Who is absent/present
Leave reasons
WFH / WFO employees
Department-wise employee details
📧 Send email notifications for leave with:
Recipient email
Custom reason/message body
🤖 Built using Agentic AI tools

🛠️ Tech Stack & Tools Used
Python
SQLite3 – Database
LangChain – Tool abstraction
LangGraph – Agent workflow orchestration
Google Gemini API
Model Used: gemini-2.5-flash
SMTP (Gmail) – Email sending
dotenv – Environment variable management

🗃️ Database Schema
**EMPLOYEE Table**
ID
NAME
DEPARTMENT
**ATTENDANCE Table**
EMP_ID (Foreign Key → EMPLOYEE.ID)
DATE
WORK_MODE (WFH / WFO)
STATUS (Present / Absent)
REASON_ABSENCE

📧 **Email Functionality**
If an employee is on leave, the bot can:
Draft an email
Include the leave reason as the email body
Send the email to the specified recipient automatically

🔐 Environment Variables Required
Create a .env file:
GEMINI_API_KEY=your_gemini_api_key
SENDER_EMAIL=your_email@gmail.com
SENDER_EMAIL_PASSWORD=your_app_password

🧠 How It Works
User asks a question in plain English
Agent decides whether to:
Generate SQL
Query the database
Send an email
SQL is generated and executed on SQLite
Results are returned to the user
Emails are sent when requested

📌 Use Cases
Smart attendance tracking
AI-powered HR assistant
Natural language to SQL automation
