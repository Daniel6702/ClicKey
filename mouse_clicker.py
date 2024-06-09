import sys
import threading
import pyautogui
import random
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QSpinBox, QLineEdit, QPushButton, QHBoxLayout, QCheckBox, QGroupBox, QStackedLayout, QRadioButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
import time
import platform

class MouseClicker(QWidget):
    def __init__(self):
        super().__init__()

        self.is_running = False
        self.thread = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_mouse_position)
        self.initUI()

    def updateSettings(self, settings):
        self.start_hotkey = settings['start_mouse_clicker_hotkey']
        self.stop_hotkey = settings['stop_mouse_clicker_hotkey']

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        self.title = QLabel("Auto Mouse Clicker")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title)

        self.status_label = QLabel("Status: Idle")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)

        # Group Box for Mouse Button and Action
        button_action_group = QGroupBox("Click Action")
        button_action_layout = QVBoxLayout()
        button_action_group.setLayout(button_action_layout)

        self.button_combo = QComboBox(self)
        self.button_combo.addItems(["left", "right", "middle", "both"])
        button_action_layout.addWidget(QLabel("Mouse Button"))
        button_action_layout.addWidget(self.button_combo)

        self.action_combo = QComboBox(self)
        self.action_combo.addItems(["single click", "double click"])
        button_action_layout.addWidget(QLabel("Action"))
        button_action_layout.addWidget(self.action_combo)

        # Group Box for Number of Clicks
        click_times_group = QGroupBox("Number of Clicks")
        click_times_layout = QVBoxLayout()
        click_times_group.setLayout(click_times_layout)

        self.repeat_until_stopped_radio = QRadioButton("Repeat Until Stopped")
        self.repeat_until_stopped_radio.setChecked(True)
        self.repeat_radio = QRadioButton("Repeat 'X' times")
        click_times_layout.addWidget(self.repeat_until_stopped_radio)
        click_times_layout.addWidget(self.repeat_radio)

        self.click_times_input = QSpinBox(self)
        self.click_times_input.setMinimum(1)
        self.click_times_input.setMaximum(1000000)
        self.click_times_input.setValue(1)
        click_times_layout.addWidget(self.click_times_input)

        temp = QHBoxLayout()
        temp.addWidget(button_action_group)
        temp.addWidget(click_times_group)
        main_layout.addLayout(temp)

        # Group Box for Click Interval
        self.interval_group = QGroupBox("Interval")
        interval_layout = QVBoxLayout()
        self.interval_group.setLayout(interval_layout)

        self.random_delay_checkbox = QCheckBox("Random interval")
        self.random_delay_checkbox.stateChanged.connect(self.update_random_delay_visibility)
        interval_layout.addWidget(self.random_delay_checkbox)

        # Create stacked layout for fixed and random interval inputs
        self.interval_stacked_layout = QStackedLayout()
        self.fixed_interval_widget = QWidget()
        self.random_interval_widget = QWidget()

        # Fixed interval layout
        fixed_interval_layout = QHBoxLayout(self.fixed_interval_widget)
        self.hours_input = QSpinBox(self)
        self.hours_input.setRange(0, 23)
        self.hours_label = QLabel("Hours")
        self.minutes_input = QSpinBox(self)
        self.minutes_input.setRange(0, 59)
        self.minute_label = QLabel("Minutes")
        self.seconds_input = QSpinBox(self)
        self.seconds_input.setRange(0, 59)
        self.seconds_label = QLabel("Seconds")
        self.milliseconds_input = QSpinBox(self)
        self.milliseconds_input.setRange(0, 999)
        self.milliseconds_label = QLabel("Milliseconds")
        fixed_interval_layout.addWidget(self.hours_label)
        fixed_interval_layout.addWidget(self.hours_input)
        fixed_interval_layout.addWidget(self.minute_label)
        fixed_interval_layout.addWidget(self.minutes_input)
        fixed_interval_layout.addWidget(self.seconds_label)
        fixed_interval_layout.addWidget(self.seconds_input)
        fixed_interval_layout.addWidget(self.milliseconds_label)
        fixed_interval_layout.addWidget(self.milliseconds_input)

        # Random interval layout
        random_interval_layout = QHBoxLayout(self.random_interval_widget)
        self.min_delay_input = QSpinBox(self)
        self.min_delay_input.setRange(0, 3600)
        self.max_delay_input = QSpinBox(self)
        self.max_delay_input.setRange(0, 3600)
        random_interval_layout.addWidget(QLabel("Min delay (s)"))
        random_interval_layout.addWidget(self.min_delay_input)
        random_interval_layout.addWidget(QLabel("Max delay (s)"))
        random_interval_layout.addWidget(self.max_delay_input)

        self.interval_stacked_layout.addWidget(self.fixed_interval_widget)
        self.interval_stacked_layout.addWidget(self.random_interval_widget)
        interval_layout.addLayout(self.interval_stacked_layout)

        main_layout.addWidget(self.interval_group)

        # Group Box for Click Position
        self.position_group = QGroupBox("Click Position")
        self.position_group.setMinimumWidth(505)
        position_layout = QVBoxLayout()
        self.position_group.setLayout(position_layout)

        temp = QHBoxLayout()
        self.mouse_position_label = QLabel("Current Mouse Position:\n (X: 0, Y: 0)")
        self.mouse_position_label.setStyleSheet("font-size: 12px; color: #555; margin-left: 45px;")
        self.position_combo = QComboBox(self)
        self.position_combo.addItems(["follow mouse", "center", "coordinates", "random position", "rectangle"])
        self.position_combo.currentIndexChanged.connect(self.update_coordinate_inputs_visibility)
        position_layout.addWidget(QLabel("Click Position:"))
        temp.addWidget(self.position_combo)
        temp.addWidget(self.mouse_position_label)

        position_layout.addLayout(temp)

        self.coord_x_input = QLineEdit(self)
        self.coord_y_input = QLineEdit(self)
        self.coord_x_label = QLabel("X Coordinate:")
        self.coord_y_label = QLabel("Y Coordinate:")

        position_layout.addWidget(self.coord_x_label)
        position_layout.addWidget(self.coord_x_input)
        position_layout.addWidget(self.coord_y_label)
        position_layout.addWidget(self.coord_y_input)

        self.rectangle_top_left_x = QLineEdit(self)
        self.rectangle_top_left_y = QLineEdit(self)
        self.rectangle_bottom_right_x = QLineEdit(self)
        self.rectangle_bottom_right_y = QLineEdit(self)
        self.rectangle_top_left_x_label = QLabel("Top Left X:")
        self.rectangle_top_left_y_label = QLabel("Top Left Y:")
        self.rectangle_bottom_right_x_label = QLabel("Bottom Right X:")
        self.rectangle_bottom_right_y_label = QLabel("Bottom Right Y:")
        position_layout.addWidget(self.rectangle_top_left_x_label)
        position_layout.addWidget(self.rectangle_top_left_x)
        position_layout.addWidget(self.rectangle_top_left_y_label)
        position_layout.addWidget(self.rectangle_top_left_y)
        position_layout.addWidget(self.rectangle_bottom_right_x_label)
        position_layout.addWidget(self.rectangle_bottom_right_x)
        position_layout.addWidget(self.rectangle_bottom_right_y_label)
        position_layout.addWidget(self.rectangle_bottom_right_y)

        main_layout.addWidget(self.position_group)

        # Sound Effect Option
        self.sound_effect_checkbox = QCheckBox("Sound effect on click")
        main_layout.addWidget(self.sound_effect_checkbox)

        # Start and Stop Buttons
        self.start_stop_layout = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.start_button.setObjectName("startButton")
        self.start_button.clicked.connect(self.start_clicker)
        self.start_stop_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setObjectName("stopButton")
        self.stop_button.clicked.connect(self.stop_clicker)
        self.start_stop_layout.addWidget(self.stop_button)

        main_layout.addLayout(self.start_stop_layout)

        self.setLayout(main_layout)
        self.update_coordinate_inputs_visibility()
        self.update_random_delay_visibility()

        # Start timer to update mouse position
        self.timer.start(100)  # Update every 100 ms

        # Apply CSS Styles
        self.applyStyles()

    def applyStyles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f9f9f9;
                font-family: Arial, sans-serif;
            }
            QGroupBox {
                border: 1px solid #d3d3d3;
                border-radius: 5px;
                margin-top: 10px;
                padding: 10px;
                font-weight: bold;
                color: #333;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px;
                background-color: #e6e6e6;
                border-radius: 5px;
            }
            QLabel {
                font-size: 14px;
                color: #555;
            }
            QLabel#title {
                font-size: 16px;
                color: #000000;
                font-weight: bold;
                margin-bottom: 10px;
                border: 1px solid #d3d3d3;
                border-radius: 5px;
                padding: 5px;
            }
            QComboBox, QSpinBox, QLineEdit {
                padding: 5px;
                margin: 5px 0;
                border: 1px solid #d3d3d3;
                border-radius: 5px;
            }
            QPushButton {
                font-size: 16px;
                color: #fff;
                background-color: #0078d7;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                margin: 10px 0;
            }
            QPushButton:hover {
                background-color: #005bb5;
            }
            QPushButton:pressed {
                background-color: #003f8a;
            }
            QPushButton:focus {
                outline: none;
            }
            QPushButton#startButton {
                background-color: #28a745;
                max-width: 100%;
            }
            QPushButton#startButton:hover {
                background-color: #218838;
                max-width: 100%;
            }
            QPushButton#startButton:pressed {
                background-color: #1e7e34;
                max-width: 100%;
            }
            QPushButton#stopButton {
                background-color: #dc3545;
                max-width: 100%;
            }
            QPushButton#stopButton:hover {
                background-color: #c82333;
                max-width: 100%;
            }
            QPushButton#stopButton:pressed {
                background-color: #bd2130;'
                max-width: 100%;
            }
        """)

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

    def update_random_delay_visibility(self):
        if self.random_delay_checkbox.isChecked():
            self.interval_stacked_layout.setCurrentWidget(self.random_interval_widget)
        else:
            self.interval_stacked_layout.setCurrentWidget(self.fixed_interval_widget)

    def update_mouse_position(self):
        pos = pyautogui.position()
        self.mouse_position_label.setText(f"Current Mouse Position:\n (X: {pos.x}, Y: {pos.y})")

    def get_interval(self):
        hours = self.hours_input.value()
        minutes = self.minutes_input.value()
        seconds = self.seconds_input.value()
        milliseconds = self.milliseconds_input.value()
        total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000.0
        return total_seconds

    def start_clicker(self):
        time.sleep(1)
        if not self.is_running:
            self.is_running = True
            self.status_label.setText("Status: Running")
            interval = self.get_interval()
            button = self.button_combo.currentText()
            position = self.position_combo.currentText()
            x = int(self.coord_x_input.text()) if self.coord_x_input.text().isdigit() else 0
            y = int(self.coord_y_input.text()) if self.coord_y_input.text().isdigit() else 0
            rect_tl_x = int(self.rectangle_top_left_x.text()) if self.rectangle_top_left_x.text().isdigit() else 0
            rect_tl_y = int(self.rectangle_top_left_y.text()) if self.rectangle_top_left_y.text().isdigit() else 0
            rect_br_x = int(self.rectangle_bottom_right_x.text()) if self.rectangle_bottom_right_x.text().isdigit() else 0
            rect_br_y = int(self.rectangle_bottom_right_y.text()) if self.rectangle_bottom_right_y.text().isdigit() else 0
            click_times_mode = "X times" if self.repeat_radio.isChecked() else "Infinite (Until Stopped)"
            click_times = self.click_times_input.value() if click_times_mode == "X times" else -1
            action = self.action_combo.currentText()
            random_delay = self.random_delay_checkbox.isChecked()
            min_delay = self.min_delay_input.value()
            max_delay = self.max_delay_input.value()
            sound_effect = self.sound_effect_checkbox.isChecked()
            self.thread = threading.Thread(target=self.click_mouse, args=(button, interval, position, x, y, rect_tl_x, rect_tl_y, rect_br_x, rect_br_y, click_times, action, random_delay, min_delay, max_delay, sound_effect))
            self.thread.start()

    def stop_clicker(self):
        if self.is_running:
            self.is_running = False
            self.status_label.setText("Status: Idle")
            if self.thread is not None:
                self.thread.join()

    def play_beep(self):
        if platform.system() == "Windows":
            import winsound
            winsound.Beep(1000, 500)
        elif platform.system() == "Darwin":
            import os
            os.system('echo -n "\a"')

    def click_mouse(self, button, interval, position, x, y, rect_tl_x, rect_tl_y, rect_br_x, rect_br_y, click_times, action, random_delay, min_delay, max_delay, sound_effect):
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
            
            if sound_effect:
                self.play_beep()

            pyautogui.sleep(interval)
            clicks += 1

    def perform_action(self, button, action, x=None, y=None):
        # Save the current cursor position
        current_pos = pyautogui.position()
        
        # Move to the target position and perform the click action
        if x is not None and y is not None:
            pyautogui.moveTo(x, y)
        
        if action == "single click":
            if button == "both":
                pyautogui.click(button="left")
                pyautogui.click(button="right")
            else:
                pyautogui.click(button=button)
        elif action == "double click":
            if button == "both":
                pyautogui.doubleClick(button="left")
                pyautogui.doubleClick(button="right")
            else:
                pyautogui.doubleClick(button=button)
        
        # Move the cursor back to the original position
        pyautogui.moveTo(current_pos)

    def get_settings(self):
        return {
            'button': self.button_combo.currentText(),
            'interval': self.get_interval(),
            'position': self.position_combo.currentText(),
            'coord_x': self.coord_x_input.text(),
            'coord_y': self.coord_y_input.text(),
            'rect_tl_x': self.rectangle_top_left_x.text(),
            'rect_tl_y': self.rectangle_top_left_y.text(),
            'rect_br_x': self.rectangle_bottom_right_x.text(),
            'rect_br_y': self.rectangle_bottom_right_y.text(),
            'click_times_mode': "X times" if self.repeat_radio.isChecked() else "Infinite (Until Stopped)",
            'click_times': self.click_times_input.value(),
            'action': self.action_combo.currentText(),
            'random_delay': self.random_delay_checkbox.isChecked(),
            'min_delay': self.min_delay_input.value(),
            'max_delay': self.max_delay_input.value(),
            'sound_effect': self.sound_effect_checkbox.isChecked(),
        }

    def updateSettings(self, settings):
        print(settings)
        self.button_combo.setCurrentText(settings['button'])
        self.hours_input.setValue(int(settings['interval']) // 3600)
        self.minutes_input.setValue((int(settings['interval']) % 3600) // 60)
        self.seconds_input.setValue(int(settings['interval']) % 60)
        self.milliseconds_input.setValue(int((settings['interval'] * 1000) % 1000))
        self.position_combo.setCurrentText(settings['position'])
        self.coord_x_input.setText(settings['coord_x'])
        self.coord_y_input.setText(settings['coord_y'])
        self.rectangle_top_left_x.setText(settings['rect_tl_x'])
        self.rectangle_top_left_y.setText(settings['rect_tl_y'])
        self.rectangle_bottom_right_x.setText(settings['rect_br_x'])
        self.rectangle_bottom_right_y.setText(settings['rect_br_y'])
        self.repeat_radio.setChecked(settings['click_times_mode'] == "X times")
        self.repeat_until_stopped_radio.setChecked(settings['click_times_mode'] == "Infinite (Until Stopped)")
        self.click_times_input.setValue(settings['click_times'])
        self.action_combo.setCurrentText(settings['action'])
        self.random_delay_checkbox.setChecked(settings['random_delay'])
        self.min_delay_input.setValue(settings['min_delay'])
        self.max_delay_input.setValue(settings['max_delay'])
        self.sound_effect_checkbox.setChecked(settings['sound_effect'])

    def get_default_settings(self):
        return {
            'button': 'left',
            'interval': 1.0,
            'position': 'follow mouse',
            'coord_x': '0',
            'coord_y': '0',
            'rect_tl_x': '0',
            'rect_tl_y': '0',
            'rect_br_x': '0',
            'rect_br_y': '0',
            'click_times_mode': 'Infinite (Until Stopped)',
            'click_times': 1,
            'action': 'single click',
            'random_delay': False,
            'min_delay': 0,
            'max_delay': 0,
            'sound_effect': False,
        }

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MouseClicker()
    ex.show()
    sys.exit(app.exec_())
