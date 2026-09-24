from flask import Flask
from flask import render_template, request, flash, redirect, url_for
from database import connect_db, get_employees, add_employee
import subprocess
import sys

app = Flask(__name__)
app.config["SECRET_KEY"] = "attendance_secret"
@app.route("/")
def main():
    employees = get_employees()
    return render_template("dashboard.html", employees = employees)

@app.route("/employees", methods=["GET", "POST"])
def employees():
    if request.method == "POST":
        employee_id = request.form["employee_id"]
        name = request.form["name"]
        department = request.form["department"]

        if employee_id == "" or name == "" or department == "":
            flash("Please fill in all fields.")
            employees = get_employees()
            return render_template("employees.html", employees=employees)

        employees = get_employees()

        for employee in employees:
            if employee[0] == employee_id:
                flash("Employee ID already exists.")
                return render_template("employees.html", employees=employees)

        add_employee(employee_id, name, department)
        return redirect(url_for("employees"))

    employees = get_employees()
    return render_template("employees.html", employees=employees)

@app.route("/edit_employee/<employee_id>", methods=["GET", "POST"])
def edit_employee(employee_id):
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT employee_id, name, department FROM employees WHERE employee_id = ?",
        (employee_id,)
    )

    employee = cursor.fetchone()

    if request.method == "POST":
        new_employee_id = request.form["employee_id"]
        name = request.form["name"]
        department = request.form["department"]

        if new_employee_id == "" or name == "" or department == "":
            flash("Please fill in all the fields")
            connection.close()
            return render_template("edit_employee.html", employee=employee)

        cursor.execute(
        "SELECT employee_id FROM employees WHERE employee_id = ?",
        (new_employee_id,)
        )

        existing_employee = cursor.fetchone()

        if new_employee_id != employee_id and existing_employee is not None:
            flash("ID Already Exists")
            connection.close()
            return render_template("edit_employee.html", employee=employee)

        cursor.execute(
        "UPDATE employees SET employee_id = ?, name = ?, department = ? WHERE employee_id = ?",
        (new_employee_id, name, department, employee_id)
        )

        connection.commit()
        connection.close()
        return redirect(url_for("employees"))

    connection.close()
    return render_template("edit_employee.html", employee=employee)

@app.route("/delete_employee/<employee_id>")
def delete_employee(employee_id):
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM employees WHERE employee_id = ?",
        (employee_id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("employees"))

@app.route("/attendance")
def attendance():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT employee_id, date, time
        FROM attendance
        ORDER BY date DESC, time DESC
    """)

    attendance_records = cursor.fetchall()

    connection.close()

    return render_template(
        "attendance.html",
        attendance_records=attendance_records
    )

@app.route("/clock_attendance")
def clock_attendance():
    return render_template("clock_attendance.html")


@app.route("/start_recognition")
def start_recognition():

    subprocess.Popen([
        sys.executable,
        "recognize_face.py"
    ])

    return redirect(url_for("clock_attendance"))

app.run()