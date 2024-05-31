import sys
import threading
import pyautogui
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox)
from PyQt5.QtCore import Qt

class AutoPresser(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.is_running = False
        self.thread = None

    def initUI(self):
        layout = QVBoxLayout()

        # Key/Mouse Selection
        self.input_type_combo = QComboBox(self)
        self.input_type_combo.addItems(["Key", "Mouse Button"])
        layout.addWidget(QLabel("Input Type:"))
        layout.addWidget(self.input_type_combo)

        # Key Input
        self.key_input = QLineEdit(self)
        layout.addWidget(QLabel("Key (for Key option):"))
        layout.addWidget(self.key_input)

        # Mouse Button Selection
        self.mouse_button_combo = QComboBox(self)
        self.mouse_button_combo.addItems(["left", "right", "middle"])
        layout.addWidget(QLabel("Mouse Button (for Mouse Button option):"))
        layout.addWidget(self.mouse_button_combo)

        # Interval
        self.interval_input = QSpinBox(self)
        self.interval_input.setMinimum(1)
        self.interval_input.setMaximum(10000)
        self.interval_input.setSuffix(" ms")
        layout.addWidget(QLabel("Interval between presses (ms):"))
        layout.addWidget(self.interval_input)

        # Start/Stop Buttons
        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_presser)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_presser)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)
        self.setWindowTitle('Auto Key/Mouse Presser')
        self.show()

    def start_presser(self):
        if not self.is_running:
            self.is_running = True
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)

            input_type = self.input_type_combo.currentText()
            interval = self.interval_input.value() / 1000.0  # Convert ms to seconds

            if input_type == "Key":
                key = self.key_input.text()
                self.thread = threading.Thread(target=self.press_key, args=(key, interval))
            else:
                button = self.mouse_button_combo.currentText()
                self.thread = threading.Thread(target=self.press_mouse, args=(button, interval))

            self.thread.start()

    def stop_presser(self):
        if self.is_running:
            self.is_running = False
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            if self.thread is not None:
                self.thread.join()

    def press_key(self, key, interval):
        while self.is_running:
            pyautogui.press(key)
            pyautogui.sleep(interval)

    def press_mouse(self, button, interval):
        while self.is_running:
            pyautogui.click(button=button)
            pyautogui.sleep(interval)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AutoPresser()
    sys.exit(app.exec_())
