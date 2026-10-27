from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import date

app = Flask(__name__)
app.secret_key = "change-this-secret-key"
DB_NAME = "attendance.db"


def get_db():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                roll_no TEXT NOT NULL UNIQUE,
                department TEXT NOT NULL
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                attendance_date TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('Present', 'Absent')),
                UNIQUE(student_id, attendance_date),
                FOREIGN KEY(student_id) REFERENCES students(id)
            )
        """)


@app.route("/", methods=["GET", "POST"])
def index():
    db = get_db()
    today = date.today().isoformat()

    if request.method == "POST":
        action = request.form.get("action")

        if action == "add_student":
            name = request.form.get("name", "").strip()
            roll_no = request.form.get("roll_no", "").strip()
            department = request.form.get("department", "").strip()

            if not name or not roll_no or not department:
                flash("Please fill in all student fields.", "error")
            else:
                try:
                    db.execute(
                        "INSERT INTO students (name, roll_no, department) VALUES (?, ?, ?)",
                        (name, roll_no, department)
                    )
                    db.commit()
                    flash("Student added successfully.", "success")
                except sqlite3.IntegrityError:
                    flash("That roll number already exists.", "error")

        elif action == "mark_attendance":
            attendance_date = request.form.get("attendance_date", today)
            statuses = request.form.to_dict(flat=True)
            students = db.execute("SELECT id FROM students").fetchall()

            for student in students:
                status = statuses.get(f"status_{student['id']}")
                if status in ("Present", "Absent"):
                    db.execute("""
                        INSERT INTO attendance (student_id, attendance_date, status)
                        VALUES (?, ?, ?)
                        ON CONFLICT(student_id, attendance_date)
                        DO UPDATE SET status = excluded.status
                    """, (student["id"], attendance_date, status))
            db.commit()
            flash("Attendance saved successfully.", "success")

        db.close()
        return redirect(url_for("index"))

    students = db.execute("""
        SELECT s.id, s.name, s.roll_no, s.department,
               a.status AS today_status
        FROM students s
        LEFT JOIN attendance a
          ON a.student_id = s.id AND a.attendance_date = ?
        ORDER BY s.roll_no
    """, (today,)).fetchall()

    records = db.execute("""
        SELECT s.name, s.roll_no, a.attendance_date, a.status
        FROM attendance a
        JOIN students s ON s.id = a.student_id
        ORDER BY a.attendance_date DESC, s.roll_no
        LIMIT 20
    """).fetchall()

    summary = db.execute("""
        SELECT s.id, s.name, s.roll_no,
               COUNT(a.id) AS total_days,
               SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) AS present_days
        FROM students s
        LEFT JOIN attendance a ON a.student_id = s.id
        GROUP BY s.id
        ORDER BY s.roll_no
    """).fetchall()

    db.close()
    return render_template(
        "index.html", students=students, records=records,
        summary=summary, today=today
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
