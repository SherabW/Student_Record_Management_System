
import sqlite3
from pathlib import Path

DB_NAME = Path(__file__).resolve().parent / "students.db"


def connect():
    return sqlite3.connect(DB_NAME)


def create_table():
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                full_name TEXT NOT NULL,
                class_name TEXT NOT NULL,
                subject TEXT NOT NULL,
                gender TEXT NOT NULL,
                contact TEXT NOT NULL,
                email TEXT,
                marks REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def add_student(data):
    with connect() as conn:
        conn.execute("""
            INSERT INTO students
            (student_id, full_name, class_name, subject,
             gender, contact, email, marks)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, data)


def get_students():
    with connect() as conn:
        return conn.execute("""
            SELECT student_id, full_name, class_name,
                   subject, gender, contact, email, marks
            FROM students
            ORDER BY student_id
        """).fetchall()


def get_student(student_id):
    with connect() as conn:
        return conn.execute("""
            SELECT student_id, full_name, class_name,
                   subject, gender, contact, email, marks
            FROM students
            WHERE student_id = ?
        """, (student_id,)).fetchone()


def update_student(student_id, data):
    with connect() as conn:
        cursor = conn.execute("""
            UPDATE students
            SET full_name = ?, class_name = ?, subject = ?,
                gender = ?, contact = ?, email = ?, marks = ?
            WHERE student_id = ?
        """, (*data, student_id))
        return cursor.rowcount


def delete_student(student_id):
    with connect() as conn:
        cursor = conn.execute(
            "DELETE FROM students WHERE student_id = ?",
            (student_id,)
        )
        return cursor.rowcount


def search_students(keyword):
    keyword = f"%{keyword}%"

    with connect() as conn:
        return conn.execute("""
            SELECT student_id, full_name, class_name,
                   subject, gender, contact, email, marks
            FROM students
            WHERE student_id LIKE ?
               OR full_name LIKE ?
               OR class_name LIKE ?
               OR subject LIKE ?
            ORDER BY student_id
        """, (keyword,) * 4).fetchall()
