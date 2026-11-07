
import csv
import re
import sqlite3
import database


class StudentService:

    @staticmethod
    def calculate_grade(marks):
        marks = float(marks)

        if marks >= 80:
            return "A"
        elif marks >= 70:
            return "B"
        elif marks >= 60:
            return "C"
        elif marks >= 50:
            return "D"
        return "F"

    @staticmethod
    def validate(data):
        student_id, name, class_name, subject, gender, contact, email, marks = data

        if not student_id.strip():
            raise ValueError("Student ID is required.")

        if not name.strip():
            raise ValueError("Student name is required.")

        if not class_name:
            raise ValueError("Please select a class.")

        if not subject:
            raise ValueError("Please select a subject.")

        if not gender:
            raise ValueError("Please select a gender.")

        if not contact.strip():
            raise ValueError("Contact number is required.")

        if not contact.isdigit():
            raise ValueError("Contact must contain digits only.")

        if email:
            pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
            if not re.fullmatch(pattern, email):
                raise ValueError("Please enter a valid email address.")

        if not 0 <= marks <= 100:
            raise ValueError("Marks must be between 0 and 100.")

    def add_student(self, data):
        self.validate(data)

        if database.get_student(data[0]):
            raise ValueError("Student ID already exists.")

        try:
            database.add_student(data)
        except sqlite3.IntegrityError:
            raise ValueError("Student ID already exists.")

    def update_student(self, student_id, data):
        self.validate((student_id, *data))

        if not database.get_student(student_id):
            raise ValueError("Student record not found.")

        database.update_student(student_id, data)

    def delete_student(self, student_id):
        if not database.delete_student(student_id):
            raise ValueError("Student record not found.")

    def export_csv(self, file_path):
        students = database.get_students()

        with open(file_path, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)

            writer.writerow([
                "Student ID", "Full Name", "Class",
                "Subject", "Gender", "Contact",
                "Email", "Marks", "Grade"
            ])

            for student in students:
                grade = self.calculate_grade(student[7])
                writer.writerow([*student, grade])
