
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("PyQt6 Hello World")

layout = QVBoxLayout(window)

message = QLabel("Hello, GUI!")
button = QPushButton("Click Me")

button.clicked.connect(
    lambda: message.setText("You clicked the PyQt6 button!")
)

layout.addWidget(message)
layout.addWidget(button)

window.show()
sys.exit(app.exec())
