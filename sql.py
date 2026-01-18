import sqlite3 

# Establish a connection to the SQLite database
connection = sqlite3.connect('attendance.db')

#create a cursor object to interact with database
cursor = connection.cursor()

table1_info = """
CREATE TABLE IF NOT EXISTS EMPLOYEE (
    ID INT PRMARY KEY NOT NULL,
    NAME VARCHAR(100) NOT NULL,
    DEPARTMENT VARCHAR(50) NOT NULL
)
"""
table2_info = '''
CREATE TABLE IF NOT EXISTS ATTENDANCE (
    EMP_ID INT NOT NULL,
    DATE DATE NOT NULL,
    WORK_MODE VARCHAR(20), 
    STATUS VARCHAR(20),
    REASON_ABSENCE VARCHAR(255),
    PRIMARY KEY (EMP_ID, DATE),
    FOREIGN KEY (EMP_ID) REFERENCES EMPLOYEE(ID)
)
'''

# Execute the table creation commands
cursor.execute(table1_info)
cursor.execute(table2_info)

#insert some dummy data into EMPLOYEE table
cursor.execute(''' INSERT INTO EMPLOYEE (ID, NAME, DEPARTMENT) VALUES(1, 'Riya Doe', 'IT') ''')
cursor.execute(''' INSERT INTO EMPLOYEE (ID, NAME, DEPARTMENT) VALUES(2, 'Elon Smith', 'HR') ''')
cursor.execute(''' INSERT INTO EMPLOYEE (ID, NAME, DEPARTMENT) VALUES(3, 'Dev Brown', 'HR') ''')
cursor.execute(''' INSERT INTO EMPLOYEE (ID, NAME, DEPARTMENT) VALUES(4, 'Gabriel Cooper', 'IT') ''')
cursor.execute(''' INSERT INTO EMPLOYEE (ID, NAME, DEPARTMENT) VALUES(5, 'Camille Wilson', 'Finance') ''')

#insert some dummy data into Attendance table
cursor.execute(''' INSERT INTO ATTENDANCE (EMP_ID, DATE, WORK_MODE, STATUS, REASON_ABSENCE) VALUES(1, '2026-01-01', 'Remote', 'Present', NULL) ''')
cursor.execute(''' INSERT INTO ATTENDANCE (EMP_ID, DATE, WORK_MODE, STATUS, REASON_ABSENCE) VALUES(2, '2026-01-01', 'Office', 'Present', NULL) ''')
cursor.execute(''' INSERT INTO ATTENDANCE (EMP_ID, DATE, WORK_MODE, STATUS, REASON_ABSENCE) VALUES(3, '2026-01-01', NULL , 'Absent', 'Sick Leave') ''')
cursor.execute(''' INSERT INTO ATTENDANCE (EMP_ID, DATE, WORK_MODE, STATUS, REASON_ABSENCE) VALUES(4, '2026-01-01', 'Remote', 'Present', NULL) ''')
cursor.execute(''' INSERT INTO ATTENDANCE (EMP_ID, DATE, WORK_MODE, STATUS, REASON_ABSENCE) VALUES(5, '2026-01-01', NULL , 'Absent','family emergency') ''')

#close the connection
connection.commit()
connection.close()
