import sys
import pyautogui
import time
import random
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QSpinBox, QCheckBox, QComboBox, QFileDialog, QApplication, QMessageBox, QGroupBox, QRadioButton, QStackedLayout)
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from pynput import keyboard, mouse
import threading

class SignalEmitter(QObject):
    text_signal = pyqtSignal(str)

class Scripts(QWidget):
    def __init__(self):
        super().__init__()
        self.process = None
        self.listener = None
        self.initUI()
        self.signal_emitter = SignalEmitter()
        self.signal_emitter.text_signal.connect(self.update_script_editor)
    
    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        self.title = QLabel("Scripts")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title) 

        self.status_label = QLabel("Status: Idle")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)

        temp3 = QVBoxLayout()
        temp4 = QHBoxLayout()

        #Script Group
        script_actions_group = QGroupBox("Script")
        script_actions_layout = QVBoxLayout()
        script_actions_group.setLayout(script_actions_layout)

        self.script_editor = QTextEdit()
        script_actions_layout.addWidget(self.script_editor)


        # Recording Options
        recording_group = QGroupBox("Script Actions")
        recording_layout = QVBoxLayout()
        recording_group.setLayout(recording_layout)

        self.record_delay_checkbox = QCheckBox("Record Delay")
        self.record_delay_checkbox.setChecked(True)
        recording_layout.addWidget(self.record_delay_checkbox)

        temp = QHBoxLayout()
        self.start_record_button = QPushButton("Start Recording")
        self.start_record_button.clicked.connect(self.start_recording)
        temp.addWidget(self.start_record_button)

        self.stop_record_button = QPushButton("Stop Recording")
        self.stop_record_button.clicked.connect(self.stop_recording)
        temp.addWidget(self.stop_record_button)

        temp2 = QHBoxLayout()
        self.load_button = QPushButton("Load Script")
        self.load_button.clicked.connect(self.load_script)
        temp2.addWidget(self.load_button)

        self.save_button = QPushButton("Save Script")
        self.save_button.clicked.connect(self.save_script)
        temp2.addWidget(self.save_button)

        recording_layout.addLayout(temp)
        recording_layout.addLayout(temp2)


        # Run Mode Settings
        run_mode_group = QGroupBox("Run Mode")
        run_mode_layout = QVBoxLayout()
        run_mode_group.setLayout(run_mode_layout)

        self.repeat_until_stopped_radio = QRadioButton("Repeat Until Stopped")
        self.repeat_until_stopped_radio.setChecked(True)
        self.repeat_radio = QRadioButton("Repeat 'X' times")
        run_mode_layout.addWidget(self.repeat_until_stopped_radio)
        run_mode_layout.addWidget(self.repeat_radio)

        self.run_times_input = QSpinBox(self)
        self.run_times_input.setMinimum(1)
        self.run_times_input.setMaximum(1000000)
        self.run_times_input.setValue(1)
        run_mode_layout.addWidget(self.run_times_input)

        temp3.addWidget(recording_group)
        temp3.addWidget(run_mode_group)
        temp4.addLayout(temp3)
        temp4.addWidget(script_actions_group)

        main_layout.addLayout(temp4)

        # Interval Settings
        interval_group = QGroupBox("Interval between Repeats")
        interval_layout = QVBoxLayout()
        interval_group.setLayout(interval_layout)

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

        main_layout.addWidget(interval_group)

        # Start and Stop Buttons for Script Execution
        self.start_stop_layout = QHBoxLayout()
        self.run_button = QPushButton("Run Script")
        self.run_button.setObjectName("startButton")
        self.run_button.clicked.connect(self.run_script)
        self.start_stop_layout.addWidget(self.run_button)

        self.stop_button = QPushButton("Stop Script")
        self.stop_button.setObjectName("stopButton")
        self.stop_button.clicked.connect(self.stop_script)
        self.start_stop_layout.addWidget(self.stop_button)

        main_layout.addLayout(self.start_stop_layout)

        self.setLayout(main_layout)

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
            QComboBox, QSpinBox, QLineEdit, QTextEdit {
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
                padding: 5px 5px;
                margin: 5px 0;
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
                padding: 10px 20px;
                margin: 10px 0;
            }
            QPushButton#startButton:hover {
                background-color: #218838;
                max-width: 100%;
                padding: 10px 20px;
                margin: 10px 0;
            }
            QPushButton#startButton:pressed {
                background-color: #1e7e34;
                max-width: 100%;
                padding: 10px 20px;
                margin: 10px 0;
            }
            QPushButton#stopButton {
                background-color: #dc3545;
                max-width: 100%;
                padding: 10px 20px;
                margin: 10px 0;
            }
            QPushButton#stopButton:hover {
                background-color: #c82333;
                max-width: 100%;
                padding: 10px 20px;
                margin: 10px 0;
            }
            QPushButton#stopButton:pressed {
                background-color: #bd2130;'
                max-width: 100%;
                padding: 10px 20px;
                margin: 10px 0;
            }
        """)

    def load_script(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Script", "",
                                                   "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as file:
                self.script_editor.setPlainText(file.read())

    def save_script(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Script", "",
                                                   "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as file:
                file.write(self.script_editor.toPlainText())

    def run_script(self):
        script_content = self.script_editor.toPlainText()
        if not script_content.strip():
            QMessageBox.warning(self, "Warning", "Script content is empty.")
            return

        actions = script_content.split('\n')
        self.status_label.setText("Status: Running Script")
        self.script_runner = ScriptRunner(actions, self.repeat_radio.isChecked(), self.repeat_until_stopped_radio.isChecked(), self.run_times_input.value(), self.get_interval(), self.random_delay_checkbox.isChecked(), self.min_delay_input.value(), self.max_delay_input.value())
        self.script_runner.start()

    def stop_script(self):
        if hasattr(self, 'script_runner') and self.script_runner.is_running:
            self.script_runner.stop()
            self.status_label.setText("Status: Idle")
            QMessageBox.information(self, "Info", "Script stopped.")
        else:
            QMessageBox.warning(self, "Warning", "No script is running.")

    def start_recording(self):
        if self.listener is None:
            self.listener = Listener(self.script_editor, self.record_delay_checkbox.isChecked())
            self.listener.signal_emitter = self.signal_emitter
            self.listener.start()
            self.status_label.setText("Status: Recording")

    def stop_recording(self):
        if self.listener:
            self.listener.stop()
            self.listener = None
            self.script_editor.setPlainText(self.script_editor.toPlainText().rsplit('\n', 1)[0])
            self.status_label.setText("Status: Idle")

    def update_random_delay_visibility(self):
        if self.random_delay_checkbox.isChecked():
            self.interval_stacked_layout.setCurrentWidget(self.random_interval_widget)
        else:
            self.interval_stacked_layout.setCurrentWidget(self.fixed_interval_widget)

    def update_script_editor(self, text):
        self.script_editor.append(text)
    
    def get_interval(self):
        if self.random_delay_checkbox.isChecked():
            return (self.min_delay_input.value(), self.max_delay_input.value())
        hours = self.hours_input.value()
        minutes = self.minutes_input.value()
        seconds = self.seconds_input.value()
        milliseconds = self.milliseconds_input.value()
        total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000.0
        return total_seconds
    
    def get_settings(self):
        return {
            'script_content': self.script_editor.toPlainText(),
            'record_delay': self.record_delay_checkbox.isChecked(),
            'interval': self.get_interval(),
            'run_mode': 'Infinite (Until Stopped)' if self.repeat_until_stopped_radio.isChecked() else 'Repeat X Times',
            'run_times': self.run_times_input.value(),
        }

    def updateSettings(self, settings):
        self.script_editor.setPlainText(settings['script_content'])
        self.record_delay_checkbox.setChecked(settings['record_delay'])
        interval = settings['interval']
        self.hours_input.setValue(int(interval // 3600))
        self.minutes_input.setValue(int((interval % 3600) // 60))
        self.seconds_input.setValue(int(interval % 60))
        self.milliseconds_input.setValue(int((interval * 1000) % 1000))
        self.repeat_until_stopped_radio.setChecked(settings['run_mode'] == 'Infinite (Until Stopped)')
        self.repeat_radio.setChecked(settings['run_mode'] == 'Repeat X Times')
        self.run_times_input.setValue(settings['run_times'])

    def get_default_settings(self):
        return {
            'script_content': '',
            'record_delay': True,
            'interval': 1.0,
            'run_mode': 'Infinite (Until Stopped)',
            'run_times': 1,
        }

class ScriptRunner(threading.Thread):
    def __init__(self, actions, repeat, repeat_inf, repeat_times, interval, random_interval, min_delay, max_delay):
        super().__init__()
        self.actions = actions
        self.repeat = repeat
        self.repeat_inf = repeat_inf
        self.repeat_times = repeat_times
        self.interval = interval
        self.random_interval = random_interval
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.is_running = True

    def run(self):
        if self.random_interval:
            interval = random.uniform(self.min_delay, self.max_delay)
        else:
            interval = self.interval

        while self.is_running:
            for action in self.actions:
                if not self.is_running:
                    break
                self.execute_action(action)
                
            if self.repeat and not self.repeat_inf:
                self.repeat_times -= 1
                if self.repeat_times <= 0:
                    break   

            time.sleep(interval)
            
    def execute_action(self, action):
        action = action.strip()
        if action.startswith("Send,"):
            keys = action.replace("Send,", "").strip()
            pyautogui.write(keys)
        elif action.startswith("Click,"):
            coords = action.replace("Click,", "").strip().split(",")
            x, y = int(coords[0]), int(coords[1])
            pyautogui.click(x, y)
        elif action.startswith("Sleep,"):
            delay = int(action.replace("Sleep,", "").strip()) / 1000.0
            time.sleep(delay)

    def stop(self):
        self.is_running = False

class Listener(threading.Thread):
    def __init__(self, editor, record_delay):
        super().__init__()
        self.editor = editor
        self.record_delay = record_delay
        self.running = True
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.signal_emitter = None
        self.last_time = time.time()

    def run(self):
        with self.keyboard_listener as kl, self.mouse_listener as ml:
            while self.running:
                kl.join(0.1)
                ml.join(0.1)

    def stop(self):
        self.running = False
        self.keyboard_listener.stop()
        self.mouse_listener.stop()

    def record_delay_func(self):
        if not self.record_delay:
            return
        current_time = time.time()
        delay = current_time - self.last_time
        self.last_time = current_time
        if self.signal_emitter and delay > 0:
            self.signal_emitter.text_signal.emit(f"Sleep, {int(delay * 1000)}")

    def on_press(self, key):
        self.record_delay_func()
        try:
            key_str = key.char
        except AttributeError:
            key_str = key.name
        if self.signal_emitter:
            self.signal_emitter.text_signal.emit(f"Send, {key_str}")

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.record_delay_func()
            if self.signal_emitter:
                self.signal_emitter.text_signal.emit(f"Click, {x}, {y}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Scripts()
    ex.resize(400, 500)
    ex.show()
    sys.exit(app.exec_())
