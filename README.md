# Student Record Management System

Reconstructed from the accompanying Unit V report. Requires Python 3.10+.

## Installation (VS Code terminal)

```bash
python -m venv .venv
```

On Windows:
```bash
.venv\Scripts\activate
python -m pip install -r requirements.txt
python main.py
```

On macOS/Linux:
```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

The SQLite database `students.db` is in the project directory. It is created automatically if missing. The ZIP includes one fictional sample record. Edit `DEVELOPER` and `STUDENT_ID` at the top of `main.py` if appropriate.

## Hello-world demonstrations

```bash
python partA/hello_pyqt6.py
python partA/hello_tkinter.py
streamlit run partA/hello_streamlit.py
```

## How to use

Fill the form and click Submit Student. Click a table row to edit or delete it. Search by ID, name, class or subject. Use Export CSV to save a spreadsheet-friendly file. Show Grades hides/displays the grade column. Help > About shows project details.

## Testing and academic integrity

Run all test cases yourself, add actual results and screenshots to the report, and acknowledge significant AI-assisted reconstruction in the references as required by your tutor. This code is a reconstruction, not recovered original source.
