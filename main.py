import sys
import threading
import pyautogui
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox, QCheckBox)
from PyQt5.QtCore import Qt

class AutoPresser(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.is_running = False
        self.thread = None

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        settings_layout = QHBoxLayout()
        settings_layout.setAlignment(Qt.AlignTop)

        # Key presser section
        key_layout = QVBoxLayout()
        key_layout.setAlignment(Qt.AlignTop)
        self.key_enable_checkbox = QCheckBox("Enable Key Presser")
        key_layout.addWidget(self.key_enable_checkbox)

        self.key_input = QLineEdit(self)
        key_layout.addWidget(QLabel("Key:"))
        key_layout.addWidget(self.key_input)
        
        # Interval
        self.key_interval_input = QSpinBox(self)
        self.key_interval_input.setMinimum(1)
        self.key_interval_input.setMaximum(10000)
        self.key_interval_input.setSuffix(" ms")
        key_layout.addWidget(QLabel("Interval between presses (ms):"))
        key_layout.addWidget(self.key_interval_input)

        settings_layout.addLayout(key_layout)

        # Mouse presser section
        mouse_layout = QVBoxLayout()
        mouse_layout.setAlignment(Qt.AlignTop)
        self.mouse_enable_checkbox = QCheckBox("Enable Mouse Presser")
        mouse_layout.addWidget(self.mouse_enable_checkbox)

        self.mouse_button_combo = QComboBox(self)
        self.mouse_button_combo.addItems(["left", "right", "middle"])
        mouse_layout.addWidget(QLabel("Mouse Button"))
        mouse_layout.addWidget(self.mouse_button_combo)

        self.mouse_interval_input = QSpinBox(self)
        self.mouse_interval_input.setMinimum(1)
        self.mouse_interval_input.setMaximum(10000)
        self.mouse_interval_input.setSuffix(" ms")
        mouse_layout.addWidget(QLabel("Interval between presses (ms):"))
        mouse_layout.addWidget(self.mouse_interval_input)

        # Click position options
        self.click_position_combo = QComboBox(self)
        self.click_position_combo.addItems(["follow mouse", "center", "coordinates"])
        self.click_position_combo.currentIndexChanged.connect(self.update_coordinate_inputs_visibility)
        mouse_layout.addWidget(QLabel("Click Position:"))
        mouse_layout.addWidget(self.click_position_combo)

        self.coord_x_input = QLineEdit(self)
        self.coord_y_input = QLineEdit(self)
        self.coord_x_label = QLabel("X Coordinate:")
        self.coord_y_label = QLabel("Y Coordinate:")
        mouse_layout.addWidget(self.coord_x_label)
        mouse_layout.addWidget(self.coord_x_input)
        mouse_layout.addWidget(self.coord_y_label)
        mouse_layout.addWidget(self.coord_y_input)

        # Click times options
        self.click_times_combo = QComboBox(self)
        self.click_times_combo.addItems(["Infinite", "X times"])
        self.click_times_combo.currentIndexChanged.connect(self.update_click_times_visibility)
        mouse_layout.addWidget(QLabel("Number of Clicks:"))
        mouse_layout.addWidget(self.click_times_combo)

        self.click_times_input = QSpinBox(self)
        self.click_times_input.setMinimum(1)
        self.click_times_input.setMaximum(1000000)
        self.click_times_input.setValue(1)
        mouse_layout.addWidget(self.click_times_input)

        settings_layout.addLayout(mouse_layout)

        main_layout.addLayout(settings_layout)

        # Start/Stop Buttons
        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_presser)
        main_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_presser)
        main_layout.addWidget(self.stop_button)

        self.setLayout(main_layout)
        self.setWindowTitle('Auto Key/Mouse Presser')
        self.show()

        self.update_coordinate_inputs_visibility()
        self.update_click_times_visibility()

    def update_coordinate_inputs_visibility(self):
        position = self.click_position_combo.currentText()
        is_coordinates = position == "coordinates"
        self.coord_x_label.setVisible(is_coordinates)
        self.coord_x_input.setVisible(is_coordinates)
        self.coord_y_label.setVisible(is_coordinates)
        self.coord_y_input.setVisible(is_coordinates)

    def update_click_times_visibility(self):
        mode = self.click_times_combo.currentText()
        is_x_times = mode == "X times"
        self.click_times_input.setVisible(is_x_times)

    def start_presser(self):
        if not self.is_running:
            self.is_running = True
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)

            if self.key_enable_checkbox.isChecked():
                interval = self.key_interval_input.value() / 1000.0  # Convert ms to seconds
                key = self.key_input.text()
                self.thread = threading.Thread(target=self.press_key, args=(key, interval))
            elif self.mouse_enable_checkbox.isChecked():
                interval = self.mouse_interval_input.value() / 1000.0  # Convert ms to seconds
                button = self.mouse_button_combo.currentText()
                position = self.click_position_combo.currentText()
                x = int(self.coord_x_input.text()) if self.coord_x_input.text().isdigit() else 0
                y = int(self.coord_y_input.text()) if self.coord_y_input.text().isdigit() else 0
                click_times_mode = self.click_times_combo.currentText()
                click_times = self.click_times_input.value() if click_times_mode == "X times" else -1
                self.thread = threading.Thread(target=self.press_mouse, args=(button, interval, position, x, y, click_times))

            if self.thread:
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

    def press_mouse(self, button, interval, position, x, y, click_times):
        clicks = 0
        while self.is_running and (click_times == -1 or clicks < click_times):
            if position == "follow mouse":
                pyautogui.click(button=button)
            elif position == "center":
                screen_width, screen_height = pyautogui.size()
                pyautogui.click(x=screen_width // 2, y=screen_height // 2, button=button)
            elif position == "coordinates":
                pyautogui.click(x=x, y=y, button=button)
            pyautogui.sleep(interval)
            clicks += 1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AutoPresser()
    sys.exit(app.exec_())
