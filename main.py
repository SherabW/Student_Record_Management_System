
import sys

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel,
    QLineEdit, QComboBox, QDoubleSpinBox,
    QPushButton, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QFormLayout, QGroupBox, QMessageBox,
    QFileDialog, QCheckBox, QHeaderView
)
from PyQt6.QtCore import Qt

import database
from student_service import StudentService


class StudentManagementSystem(QMainWindow):

    def __init__(self):
        super().__init__()

        self.service = StudentService()
        self.selected_id = None

        self.setWindowTitle(
            "Student Record Management System | Sherab Wangdi"
        )
        self.resize(1100, 750)
        self.setMinimumSize(850, 600)

        self.create_ui()
        self.apply_style()
        self.show_all_students()

    def create_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(12)

        # Application title
        title = QLabel("STUDENT RECORD MANAGEMENT SYSTEM")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        self.total_label = QLabel("Total Students: 0")
        main_layout.addWidget(self.total_label)

        # Student information section
        form_group = QGroupBox("Student Information")
        grid = QGridLayout(form_group)

        left_form = QFormLayout()
        right_form = QFormLayout()

        # Student ID
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Enter Student ID")

        # Full Name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter Full Name")

        # Class: PP to 12
        self.class_input = QComboBox()
        self.class_input.addItems([
            "Select Your Class",
            "PP", "1", "2", "3", "4", "5", "6",
            "7", "8", "9", "10", "11", "12"
        ])

        # Subjects
        self.subject_input = QComboBox()
        self.subject_input.addItems([
            "Select Subject",
            "DTI",
            "Mathematics",
            "English",
            "Science",
            "Dzongkha",
            "Physics",
            "Chemistry",
            "Biology"
        ])

        # Gender
        self.gender_input = QComboBox()
        self.gender_input.addItems([
            "Select Gender",
            "Male",
            "Female",
            "Other"
        ])

        # Contact number
        self.contact_input = QLineEdit()
        self.contact_input.setPlaceholderText("Enter Contact Number")

        # Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter Email (Optional)")

        # Marks
        self.marks_input = QDoubleSpinBox()
        self.marks_input.setRange(0, 100)
        self.marks_input.setDecimals(2)
        self.marks_input.setSuffix(" / 100")

        # Arrange form fields
        left_form.addRow("Student ID:", self.id_input)
        left_form.addRow("Full Name:", self.name_input)
        left_form.addRow("Class:", self.class_input)
        left_form.addRow("Subject:", self.subject_input)

        right_form.addRow("Gender:", self.gender_input)
        right_form.addRow("Contact:", self.contact_input)
        right_form.addRow("Email:", self.email_input)
        right_form.addRow("Marks:", self.marks_input)

        grid.addLayout(left_form, 0, 0)
        grid.addLayout(right_form, 0, 1)

        main_layout.addWidget(form_group)

        # Action buttons
        button_layout = QHBoxLayout()

        self.submit_button = QPushButton("Submit Student")
        self.update_button = QPushButton("Update Student")
        self.delete_button = QPushButton("Delete Student")
        self.clear_button = QPushButton("Clear Form")
        self.export_button = QPushButton("Export CSV")

        for button in [
            self.submit_button,
            self.update_button,
            self.delete_button,
            self.clear_button,
            self.export_button
        ]:
            button_layout.addWidget(button)

        main_layout.addLayout(button_layout)

        # Search section
        search_group = QGroupBox("Search Student Records")
        search_layout = QHBoxLayout(search_group)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Search by ID, Name, Class or Subject"
        )

        self.search_button = QPushButton("Search")
        self.show_all_button = QPushButton("Show All")

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        search_layout.addWidget(self.show_all_button)

        main_layout.addWidget(search_group)

        # Grade visibility checkbox
        self.grade_checkbox = QCheckBox("Show Grades")
        self.grade_checkbox.setChecked(True)
        main_layout.addWidget(self.grade_checkbox)

        # Student records table
        table_group = QGroupBox("Student Records")
        table_layout = QVBoxLayout(table_group)

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "Student ID",
            "Full Name",
            "Class",
            "Subject",
            "Gender",
            "Contact",
            "Email",
            "Marks",
            "Grade"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )

        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.table.setAlternatingRowColors(True)

        table_layout.addWidget(self.table)
        main_layout.addWidget(table_group)

        # Help menu and About dialog
        help_menu = self.menuBar().addMenu("Help")
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.show_about)

        # Status bar
        self.statusBar().showMessage("Ready")

        # Signals and slots
        self.submit_button.clicked.connect(self.add_student)
        self.update_button.clicked.connect(self.update_student)
        self.delete_button.clicked.connect(self.delete_student)
        self.clear_button.clicked.connect(self.clear_form)
        self.export_button.clicked.connect(self.export_csv)

        self.search_button.clicked.connect(self.search_students)
        self.show_all_button.clicked.connect(self.show_all_students)
        self.search_input.returnPressed.connect(self.search_students)

        self.table.cellClicked.connect(self.select_student)
        self.grade_checkbox.toggled.connect(self.toggle_grades)

    # Get data from the form
    def get_form_data(self):
        return (
            self.id_input.text().strip(),
            self.name_input.text().strip(),
            self.class_input.currentText()
            if self.class_input.currentIndex() > 0 else "",
            self.subject_input.currentText()
            if self.subject_input.currentIndex() > 0 else "",
            self.gender_input.currentText()
            if self.gender_input.currentIndex() > 0 else "",
            self.contact_input.text().strip(),
            self.email_input.text().strip(),
            self.marks_input.value()
        )

    # Add student
    def add_student(self):
        try:
            data = self.get_form_data()
            self.service.add_student(data)

            QMessageBox.information(
                self, "Success", "Student added successfully."
            )

            self.show_all_students()
            self.clear_form()
            self.statusBar().showMessage("Student added successfully.")

        except ValueError as error:
            QMessageBox.warning(self, "Validation Error", str(error))
        except Exception as error:
            QMessageBox.critical(self, "Error", str(error))

    # Update student
    def update_student(self):
        if not self.selected_id:
            QMessageBox.warning(
                self, "Warning", "Please select a student to update."
            )
            return

        try:
            data = self.get_form_data()[1:]
            self.service.update_student(self.selected_id, data)

            QMessageBox.information(
                self, "Success", "Student updated successfully."
            )

            self.show_all_students()
            self.clear_form()
            self.statusBar().showMessage("Student updated successfully.")

        except ValueError as error:
            QMessageBox.warning(self, "Validation Error", str(error))
        except Exception as error:
            QMessageBox.critical(self, "Error", str(error))

    # Delete student
    def delete_student(self):
        if not self.selected_id:
            QMessageBox.warning(
                self, "Warning", "Please select a student to delete."
            )
            return

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this student?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.service.delete_student(self.selected_id)

                QMessageBox.information(
                    self, "Success", "Student deleted successfully."
                )

                self.show_all_students()
                self.clear_form()
                self.statusBar().showMessage("Student deleted successfully.")

            except Exception as error:
                QMessageBox.critical(self, "Error", str(error))

    # Clear form
    def clear_form(self):
        self.id_input.clear()
        self.name_input.clear()
        self.class_input.setCurrentIndex(0)
        self.subject_input.setCurrentIndex(0)
        self.gender_input.setCurrentIndex(0)
        self.contact_input.clear()
        self.email_input.clear()
        self.marks_input.setValue(0)

        self.selected_id = None
        self.id_input.setReadOnly(False)
        self.table.clearSelection()

    # Display students in table
    def display_students(self, students):
        self.table.setRowCount(len(students))

        for row, student in enumerate(students):
            grade = self.service.calculate_grade(student[7])
            values = [*student, grade]

            for column, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row, column, item)

        self.table.setColumnHidden(
            8, not self.grade_checkbox.isChecked()
        )

    # Show all student records
    def show_all_students(self):
        try:
            students = database.get_students()
            self.display_students(students)

            self.total_label.setText(
                f"Total Students: {len(students)}"
            )
            self.statusBar().showMessage("All student records displayed.")

        except Exception as error:
            QMessageBox.critical(self, "Database Error", str(error))

    # Search students
    def search_students(self):
        keyword = self.search_input.text().strip()

        if not keyword:
            self.show_all_students()
            return

        try:
            students = database.search_students(keyword)
            self.display_students(students)

            self.statusBar().showMessage(
                f"{len(students)} matching record(s) found."
            )

        except Exception as error:
            QMessageBox.critical(self, "Search Error", str(error))

    # Select a student from the table
    def select_student(self, row, column):
        item = self.table.item(row, 0)

        if item is None:
            return

        student_id = item.text()
        student = database.get_student(student_id)

        if student:
            self.selected_id = student[0]

            self.id_input.setText(student[0])
            self.id_input.setReadOnly(True)

            self.name_input.setText(student[1])
            self.class_input.setCurrentText(student[2])
            self.subject_input.setCurrentText(student[3])
            self.gender_input.setCurrentText(student[4])
            self.contact_input.setText(student[5])
            self.email_input.setText(student[6] or "")
            self.marks_input.setValue(student[7])

    # Show or hide grades
    def toggle_grades(self, checked):
        self.table.setColumnHidden(8, not checked)

    # Export student records
    def export_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Student Records",
            "student_records.csv",
            "CSV Files (*.csv)"
        )

        if file_path:
            try:
                self.service.export_csv(file_path)

                QMessageBox.information(
                    self, "Success", "Records exported successfully."
                )

                self.statusBar().showMessage("CSV export completed.")

            except Exception as error:
                QMessageBox.critical(self, "Export Error", str(error))

    # About dialog
    def show_about(self):
        QMessageBox.about(
            self,
            "About",
            "Student Record Management System\n\n"
            "Developed by: Sherab Wangdi\n"
            "Student ID: 08230190\n\n"
            "Framework: PyQt6\n"
            "Database: SQLite\n"
            "Module: GUI Programming with Python"
        )

    # Professional blue styling
    def apply_style(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f4f7fb;
            }

            QLabel {
                font-size: 12px;
                color: #26384a;
            }

            QLabel#title {
                background-color: #173b63;
                color: white;
                font-size: 20px;
                font-weight: bold;
                padding: 16px;
                border-radius: 6px;
            }

            QGroupBox {
                font-size: 13px;
                font-weight: bold;
                border: 1px solid #ccd8e5;
                border-radius: 6px;
                margin-top: 12px;
                padding: 12px;
                background-color: white;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 5px;
            }

            QLineEdit, QComboBox, QDoubleSpinBox {
                padding: 7px;
                border: 1px solid #cbd5e1;
                border-radius: 4px;
                background-color: white;
            }

            QPushButton {
                background-color: #205493;
                color: white;
                padding: 9px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #173b63;
            }

            QTableWidget {
                background-color: white;
                alternate-background-color: #eef4fa;
                gridline-color: #dbe3ed;
            }

            QHeaderView::section {
                background-color: #173b63;
                color: white;
                padding: 8px;
                font-weight: bold;
            }

            QTableWidget::item:selected {
                background-color: #a8c7e8;
                color: black;
            }
        """)


# Run application
if __name__ == "__main__":
    database.create_table()

    app = QApplication(sys.argv)
    window = StudentManagementSystem()
    window.show()

    sys.exit(app.exec())
