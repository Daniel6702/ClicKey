import sys
import threading
import pyautogui
import random
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QSpinBox, QLineEdit, QPushButton, QHBoxLayout, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

class MouseClicker(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.is_running = False
        self.thread = None

    def updateSettings(self, settings):
        self.start_hotkey = settings['start_mouse_clicker_hotkey']
        self.stop_hotkey = settings['stop_mouse_clicker_hotkey']

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        self.button_combo = QComboBox(self)
        self.button_combo.addItems(["left", "right", "middle", "both"])
        layout.addWidget(QLabel("Mouse Button"))
        layout.addWidget(self.button_combo)

        layout.addWidget(QLabel("Interval between clicks:"))
        interval_layout = QHBoxLayout()
        self.hours_input = QSpinBox(self)
        self.hours_input.setRange(0, 23)
        self.minutes_input = QSpinBox(self)
        self.minutes_input.setRange(0, 59)
        self.seconds_input = QSpinBox(self)
        self.seconds_input.setRange(0, 59)
        self.milliseconds_input = QSpinBox(self)
        self.milliseconds_input.setRange(0, 999)
        interval_layout.addWidget(QLabel("Hours"))
        interval_layout.addWidget(self.hours_input)
        interval_layout.addWidget(QLabel("Minutes"))
        interval_layout.addWidget(self.minutes_input)
        interval_layout.addWidget(QLabel("Seconds"))
        interval_layout.addWidget(self.seconds_input)
        interval_layout.addWidget(QLabel("Milliseconds"))
        interval_layout.addWidget(self.milliseconds_input)
        layout.addLayout(interval_layout)

        self.random_delay_checkbox = QCheckBox("Random delay within range")
        self.random_delay_checkbox.stateChanged.connect(self.update_random_delay_visibility)
        layout.addWidget(self.random_delay_checkbox)

        self.random_delay_layout = QHBoxLayout()
        self.min_delay_input = QSpinBox(self)
        self.min_delay_input.setRange(0, 3600)
        self.max_delay_input = QSpinBox(self)
        self.max_delay_input.setRange(0, 3600)
        self.random_delay_layout.addWidget(QLabel("Min delay (s)"))
        self.random_delay_layout.addWidget(self.min_delay_input)
        self.random_delay_layout.addWidget(QLabel("Max delay (s)"))
        self.random_delay_layout.addWidget(self.max_delay_input)
        layout.addLayout(self.random_delay_layout)

        self.action_combo = QComboBox(self)
        self.action_combo.addItems(["single click", "double click"])
        layout.addWidget(QLabel("Action"))
        layout.addWidget(self.action_combo)

        self.position_combo = QComboBox(self)
        self.position_combo.addItems(["follow mouse", "center", "coordinates", "random position", "rectangle"])
        self.position_combo.currentIndexChanged.connect(self.update_coordinate_inputs_visibility)
        layout.addWidget(QLabel("Click Position:"))
        layout.addWidget(self.position_combo)

        self.coord_x_input = QLineEdit(self)
        self.coord_y_input = QLineEdit(self)
        self.coord_x_label = QLabel("X Coordinate:")
        self.coord_y_label = QLabel("Y Coordinate:")
        layout.addWidget(self.coord_x_label)
        layout.addWidget(self.coord_x_input)
        layout.addWidget(self.coord_y_label)
        layout.addWidget(self.coord_y_input)

        self.rectangle_top_left_x = QLineEdit(self)
        self.rectangle_top_left_y = QLineEdit(self)
        self.rectangle_bottom_right_x = QLineEdit(self)
        self.rectangle_bottom_right_y = QLineEdit(self)
        self.rectangle_top_left_x_label = QLabel("Top Left X:")
        self.rectangle_top_left_y_label = QLabel("Top Left Y:")
        self.rectangle_bottom_right_x_label = QLabel("Bottom Right X:")
        self.rectangle_bottom_right_y_label = QLabel("Bottom Right Y:")
        layout.addWidget(self.rectangle_top_left_x_label)
        layout.addWidget(self.rectangle_top_left_x)
        layout.addWidget(self.rectangle_top_left_y_label)
        layout.addWidget(self.rectangle_top_left_y)
        layout.addWidget(self.rectangle_bottom_right_x_label)
        layout.addWidget(self.rectangle_bottom_right_x)
        layout.addWidget(self.rectangle_bottom_right_y_label)
        layout.addWidget(self.rectangle_bottom_right_y)

        self.click_times_combo = QComboBox(self)
        self.click_times_combo.addItems(["Infinite (Until Stopped)", "X times"])
        self.click_times_combo.currentIndexChanged.connect(self.update_click_times_visibility)
        layout.addWidget(QLabel("Number of Clicks:"))
        layout.addWidget(self.click_times_combo)

        self.click_times_input = QSpinBox(self)
        self.click_times_input.setMinimum(1)
        self.click_times_input.setMaximum(1000000)
        self.click_times_input.setValue(1)
        layout.addWidget(self.click_times_input)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_clicker)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_clicker)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)
        self.update_coordinate_inputs_visibility()
        self.update_click_times_visibility()
        self.update_random_delay_visibility()

    def update_coordinate_inputs_visibility(self):
        position = self.position_combo.currentText()
        is_coordinates = position == "coordinates"
        is_rectangle = position == "rectangle"
        self.coord_x_label.setVisible(is_coordinates)
        self.coord_x_input.setVisible(is_coordinates)
        self.coord_y_label.setVisible(is_coordinates)
        self.coord_y_input.setVisible(is_coordinates)
        self.rectangle_top_left_x_label.setVisible(is_rectangle)
        self.rectangle_top_left_x.setVisible(is_rectangle)
        self.rectangle_top_left_y_label.setVisible(is_rectangle)
        self.rectangle_top_left_y.setVisible(is_rectangle)
        self.rectangle_bottom_right_x_label.setVisible(is_rectangle)
        self.rectangle_bottom_right_x.setVisible(is_rectangle)
        self.rectangle_bottom_right_y_label.setVisible(is_rectangle)
        self.rectangle_bottom_right_y.setVisible(is_rectangle)

    def update_click_times_visibility(self):
        mode = self.click_times_combo.currentText()
        is_x_times = mode == "X times"
        self.click_times_input.setVisible(is_x_times)

    def update_random_delay_visibility(self):
        is_random_delay = self.random_delay_checkbox.isChecked()
        for i in range(self.random_delay_layout.count()):
            self.random_delay_layout.itemAt(i).widget().setVisible(is_random_delay)

    def get_interval(self):
        hours = self.hours_input.value()
        minutes = self.minutes_input.value()
        seconds = self.seconds_input.value()
        milliseconds = self.milliseconds_input.value()
        total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000.0
        return total_seconds

    def start_clicker(self):
        if not self.is_running:
            self.is_running = True
            interval = self.get_interval()
            button = self.button_combo.currentText()
            position = self.position_combo.currentText()
            x = int(self.coord_x_input.text()) if self.coord_x_input.text().isdigit() else 0
            y = int(self.coord_y_input.text()) if self.coord_y_input.text().isdigit() else 0
            rect_tl_x = int(self.rectangle_top_left_x.text()) if self.rectangle_top_left_x.text().isdigit() else 0
            rect_tl_y = int(self.rectangle_top_left_y.text()) if self.rectangle_top_left_y.text().isdigit() else 0
            rect_br_x = int(self.rectangle_bottom_right_x.text()) if self.rectangle_bottom_right_x.text().isdigit() else 0
            rect_br_y = int(self.rectangle_bottom_right_y.text()) if self.rectangle_bottom_right_y.text().isdigit() else 0
            click_times_mode = self.click_times_combo.currentText()
            click_times = self.click_times_input.value() if click_times_mode == "X times" else -1
            action = self.action_combo.currentText()
            random_delay = self.random_delay_checkbox.isChecked()
            min_delay = self.min_delay_input.value()
            max_delay = self.max_delay_input.value()
            self.thread = threading.Thread(target=self.click_mouse, args=(button, interval, position, x, y, rect_tl_x, rect_tl_y, rect_br_x, rect_br_y, click_times, action, random_delay, min_delay, max_delay))
            self.thread.start()

    def stop_clicker(self):
        if self.is_running:
            self.is_running = False
            if self.thread is not None:
                self.thread.join()

    def click_mouse(self, button, interval, position, x, y, rect_tl_x, rect_tl_y, rect_br_x, rect_br_y, click_times, action, random_delay, min_delay, max_delay):
        clicks = 0
        while self.is_running and (click_times == -1 or clicks < click_times):
            if random_delay:
                interval = random.uniform(min_delay, max_delay)

            if position == "follow mouse":
                self.perform_action(button, action)
            elif position == "center":
                screen_width, screen_height = pyautogui.size()
                self.perform_action(button, action, screen_width // 2, screen_height // 2)
            elif position == "coordinates":
                self.perform_action(button, action, x, y)
            elif position == "random position":
                screen_width, screen_height = pyautogui.size()
                random_x = random.randint(0, screen_width)
                random_y = random.randint(0, screen_height)
                self.perform_action(button, action, random_x, random_y)
            elif position == "rectangle":
                random_x = random.randint(rect_tl_x, rect_br_x)
                random_y = random.randint(rect_tl_y, rect_br_y)
                self.perform_action(button, action, random_x, random_y)
            pyautogui.sleep(interval)
            clicks += 1

    def perform_action(self, button, action, x=None, y=None):
        if action == "single click":
            if button == "both":
                pyautogui.click(x=x, y=y, button="left")
                pyautogui.click(x=x, y=y, button="right")
            else:
                pyautogui.click(x=x, y=y, button=button)
        elif action == "double click":
            if button == "both":
                pyautogui.doubleClick(x=x, y=y, button="left")
                pyautogui.doubleClick(x=x, y=y, button="right")
            else:
                pyautogui.doubleClick(x=x, y=y, button=button)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MouseClicker()
    ex.show()
    sys.exit(app.exec_())
