import sqlite3
from datetime import datetime

def connect_db():
    connection = sqlite3.connect("attendance.db")
    
    return connection

def create_table():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id TEXT,
    name TEXT,
    department TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id TEXT,
        date TEXT,
        time TEXT)
    """)
    
    connection.commit()
    connection.close()

def add_employee(employee_id, name, department):
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO employees (employee_id, name, department)
    VALUES (?,?,?)
    """, (employee_id, name, department))
    connection.commit()
    connection.close()

def get_employees():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT employee_id, name, department
        FROM employees
    """)

    employees = cursor.fetchall()
    connection.close()

    return employees

def record_attendance(employee_id):
    connection = connect_db()
    cursor = connection.cursor()

    now = datetime.now()

    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    cursor.execute(
        """
        INSERT INTO attendance (employee_id, date, time)
        VALUES (?, ?, ?)
        """,
        (employee_id, date, time)
    )

    connection.commit()
    connection.close()

def clear_employees():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute('''
    DELETE FROM employees
    ''')
    connection.commit()
    connection.close()

create_table()