#!/usr/bin/env python3

import shlex
import subprocess
import sys
from datetime import datetime, time

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

# ----------------------------
# CONFIG
# ----------------------------
WORK_START = time(0, 0)
WORK_END = time(23, 0)

PASSWORD = "3.1415926535897932384"  # change this


# ----------------------------
# TIME CHECK
# ----------------------------
def is_work_time():
    now = datetime.now().time()
    return WORK_START <= now <= WORK_END


def launch_app(app_cmd):
    try:
        subprocess.Popen(shlex.split(app_cmd))
    except Exception as e:
        print(f"Error launching app: {e}")


# ----------------------------
# GUI
# ----------------------------
class BlockWindow(QWidget):
    def __init__(self, app_cmd):
        super().__init__()

        self.app_cmd = app_cmd

        self.setWindowTitle("Blocked")
        self.setFixedSize(400, 250)

        layout = QVBoxLayout()

        label = QLabel(
            f"Is this app really necessary to use right now?.\n\nBlocked: {app_cmd}"
        )

        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.returnPressed.connect(self.check_password)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        unlock_button = QPushButton("Unlock")
        unlock_button.clicked.connect(self.check_password)

        layout.addWidget(label)
        layout.addWidget(self.password_input)
        layout.addWidget(unlock_button)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def check_password(self):
        if self.password_input.text() == PASSWORD:
            launch_app(self.app_cmd)
            QApplication.quit()
        else:
            self.status_label.setText("Incorrect password")


# ----------------------------
# MAIN LOGIC
# ----------------------------
def main():
    if len(sys.argv) < 2:
        print('Usage: focus_launcher.py "command"')
        sys.exit(1)

    app_cmd = sys.argv[1]

    if is_work_time():
        app = QApplication(sys.argv)

        window = BlockWindow(app_cmd)
        window.show()

        sys.exit(app.exec())

    launch_app(app_cmd)


if __name__ == "__main__":
    main()
