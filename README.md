# Attendance Management System

A beginner-friendly Cloud Computing mini project built with Python, Flask, HTML/CSS, and SQLite.

## Features
- Add student details (name, roll number, department)
- Mark attendance as Present or Absent for a selected date
- Update attendance for a student/date without creating duplicate entries
- View attendance percentage and recent records
- Save data in a local SQLite database

## Requirements
- Python 3.10 or later
- pip

## Run locally

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Create a virtual environment (recommended):

   ```bash
   python -m venv venv
   ```

4. Activate it:

   **Windows**
   ```bash
   venv\Scripts\activate
   ```

   **macOS/Linux**
   ```bash
   source venv/bin/activate
   ```

5. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Start the app:

   ```bash
   python app.py
   ```

7. Open `http://127.0.0.1:5000` in your browser.

The SQLite database (`attendance.db`) is created automatically when the app starts.

## Sample test data

Add these sample students through the form:

| Student Name | Roll Number | Department |
|---|---|---|
| Anu Kumar | CSE001 | CSE |
| Ravi Kumar | CSE002 | CSE |

Then mark attendance for the date shown on the page and save.

## Sample output

```text
Attendance Management System

Add Student
Student Name: Anu Kumar
Roll Number: CSE001
Department: CSE
[Add Student]

Mark Attendance
CSE001 | Anu Kumar | CSE | Present
CSE002 | Ravi Kumar | CSE | Absent
[Save Attendance]

Attendance Percentage
CSE001 | Anu Kumar | Days Marked: 1 | Present: 1 | 100.0%
CSE002 | Ravi Kumar | Days Marked: 1 | Present: 0 | 0.0%
```

The exact date displayed depends on the day you run the program.

## Cloud computing connection

This version runs locally for development. To make it a cloud project, deploy the Flask app to a cloud hosting service and use a persistent database. SQLite is suitable for a small demo, but for a multi-user production deployment use a managed database such as PostgreSQL. Do not store real student personal data in a public demo.

## Limitations
- No login or role-based access yet.
- SQLite is intended for a small demonstration.
- Attendance is entered manually.

## Future enhancements
- Admin/teacher login
- Student login and attendance history
- Export attendance to CSV
- Cloud database and cloud deployment
- Email notifications for low attendance

## License
For educational use.
