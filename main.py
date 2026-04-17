#!/usr/bin/env python3

import subprocess
import sys
from datetime import datetime, time

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

# ----------------------------
# CONFIG
# ----------------------------
WORK_START = time(8, 0)  # 08:00
WORK_END = time(18, 0)  # 18:00


# ----------------------------
# TIME CHECK
# ----------------------------
def is_work_time():
    now = datetime.now().time()
    return WORK_START <= now <= WORK_END


# ----------------------------
# GUI WARNING
# ----------------------------
class BlockWindow(QWidget):
    def __init__(self, app_name):
        super().__init__()

        self.setWindowTitle("Blocked")
        self.setFixedSize(400, 200)

        layout = QVBoxLayout()

        label = QLabel(f"Not time for distraction.\n\nBlocked: {app_name}")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 16px;")

        layout.addWidget(label)
        self.setLayout(layout)


# ----------------------------
# MAIN LOGIC
# ----------------------------
def main():
    if len(sys.argv) < 2:
        print('Usage: ./focus_launcher "app_name"')
        sys.exit(1)

    app_name = sys.argv[1]

    # If it's work time AND app is blocked → show warning
    if is_work_time():
        app = QApplication(sys.argv)

        window = BlockWindow(app_name)
        window.show()

        sys.exit(app.exec())

    # Otherwise → run the app
    try:
        subprocess.Popen(app_name.split())
    except Exception as e:
        print(f"Error launching app: {e}")


if __name__ == "__main__":
    main()
