
from flask import Flask, request
from flask_smorest import abort

from db import get_db_connection, create_tables

import sqlite3

app = Flask(__name__)

# Create the database tables when the application starts
create_tables()


# =========================================
# HELPER: GET STUDENT WITH THEIR REPORTS
# =========================================

def get_student_data(student_id):
    connection = get_db_connection()

    student = connection.execute(
        "SELECT * FROM student WHERE id = ?",
        (student_id,)
    ).fetchone()

    if student is None:
        connection.close()
        return None

    reports = connection.execute(
        "SELECT * FROM report WHERE student_id = ?",
        (student_id,)
    ).fetchall()

    result = dict(student)
    result["reports"] = [dict(report) for report in reports]

    connection.close()
    return result


# =========================================
# 1. REPORT ENDPOINTS
# =========================================

@app.get("/report/<int:report_id>")
def get_report(report_id):
    connection = get_db_connection()

    report = connection.execute(
        "SELECT * FROM report WHERE id = ?",
        (report_id,)
    ).fetchone()

    connection.close()

    if report is None:
        abort(404, message="Report not found")

    return dict(report)


@app.post("/report")
def create_report():
    report_data = request.get_json(silent=True)

    if not isinstance(report_data, dict):
        abort(400, message="JSON object required")

    if (
        "title" not in report_data
        or "type" not in report_data
        or "student_id" not in report_data
    ):
        abort(
            400,
            message="Missing required fields: title, type and student_id"
        )

    connection = get_db_connection()

    student = connection.execute(
        "SELECT id FROM student WHERE id = ?",
        (report_data["student_id"],)
    ).fetchone()

    if student is None:
        connection.close()
        abort(404, message="Student not found")

    duplicate = connection.execute(
        """SELECT id FROM report
           WHERE title = ? AND type = ? AND student_id = ?""",
        (
            report_data["title"],
            report_data["type"],
            report_data["student_id"]
        )
    ).fetchone()

    if duplicate:
        connection.close()
        abort(400, message="Report with the same title already exists")

    cursor = connection.execute(
        """INSERT INTO report (title, type, student_id)
           VALUES (?, ?, ?)""",
        (
            report_data["title"],
            report_data["type"],
            report_data["student_id"]
        )
    )

    connection.commit()

    report = connection.execute(
        "SELECT * FROM report WHERE id = ?",
        (cursor.lastrowid,)
    ).fetchone()

    connection.close()

    return dict(report), 201


@app.delete("/report/<int:report_id>")
def delete_report(report_id):
    connection = get_db_connection()

    cursor = connection.execute(
        "DELETE FROM report WHERE id = ?",
        (report_id,)
    )

    connection.commit()
    connection.close()

    if cursor.rowcount == 0:
        abort(404, message="Report not found")

    return {"message": "Report deleted successfully"}


@app.put("/report/<int:report_id>")
def update_report(report_id):
    report_data = request.get_json(silent=True)

    if not isinstance(report_data, dict):
        abort(400, message="JSON object required")

    if "title" not in report_data or "type" not in report_data:
        abort(400, message="Missing required fields: title and type")

    connection = get_db_connection()

    report = connection.execute(
        "SELECT * FROM report WHERE id = ?",
        (report_id,)
    ).fetchone()

    if report is None:
        connection.close()
        abort(404, message="Report not found")

    connection.execute(
        "UPDATE report SET title = ?, type = ? WHERE id = ?",
        (report_data["title"], report_data["type"], report_id)
    )

    connection.commit()

    updated_report = connection.execute(
        "SELECT * FROM report WHERE id = ?",
        (report_id,)
    ).fetchone()

    connection.close()

    return dict(updated_report)


@app.get("/report")
def get_all_reports():
    connection = get_db_connection()

    reports = connection.execute(
        "SELECT * FROM report"
    ).fetchall()

    connection.close()

    return {"reports": [dict(report) for report in reports]}


# =========================================
# 2. STUDENT ENDPOINTS
# =========================================

@app.get("/student/<int:student_id>")
def get_student(student_id):
    student = get_student_data(student_id)

    if student is None:
        abort(404, message="Student not found")

    return student


@app.post("/student")
def add_student():
    student_data = request.get_json(silent=True)

    if not isinstance(student_data, dict):
        abort(400, message="JSON object required")

    if "fname" not in student_data or "lname" not in student_data:
        abort(400, message="Missing required fields: fname and lname")

    connection = get_db_connection()

    duplicate = connection.execute(
        "SELECT id FROM student WHERE fname = ? AND lname = ?",
        (student_data["fname"], student_data["lname"])
    ).fetchone()

    if duplicate:
        connection.close()
        abort(400, message="Student with the same name already exists")

    cursor = connection.execute(
        "INSERT INTO student (fname, lname) VALUES (?, ?)",
        (student_data["fname"], student_data["lname"])
    )

    connection.commit()
    student_id = cursor.lastrowid
    connection.close()

    student = get_student_data(student_id)

    return student, 201


@app.get("/student")
def get_students():
    connection = get_db_connection()

    students = connection.execute(
        "SELECT * FROM student"
    ).fetchall()

    connection.close()

    result = []

    for student in students:
        result.append(get_student_data(student["id"]))

    return {"students": result}


@app.put("/student/<int:student_id>")
def update_student(student_id):
    student_data = request.get_json(silent=True)

    if not isinstance(student_data, dict):
        abort(400, message="JSON object required")

    if "fname" not in student_data or "lname" not in student_data:
        abort(400, message="Missing required fields: fname and lname")

    connection = get_db_connection()

    student = connection.execute(
        "SELECT id FROM student WHERE id = ?",
        (student_id,)
    ).fetchone()

    if student is None:
        connection.close()
        abort(404, message="Student not found")

    connection.execute(
        "UPDATE student SET fname = ?, lname = ? WHERE id = ?",
        (student_data["fname"], student_data["lname"], student_id)
    )

    connection.commit()
    connection.close()

    return get_student_data(student_id)


@app.delete("/student/<int:student_id>")
def delete_student(student_id):
    connection = get_db_connection()

    cursor = connection.execute(
        "DELETE FROM student WHERE id = ?",
        (student_id,)
    )

    connection.commit()
    connection.close()

    if cursor.rowcount == 0:
        abort(404, message="Student not found")

    return {"message": "Student deleted successfully"}


# =========================================
# RUN APPLICATION
# =========================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
