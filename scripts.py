import sys
import subprocess
import os
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QSpinBox, QCheckBox, QComboBox, QFileDialog, QApplication, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from pynput import keyboard, mouse
import threading
import time

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
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        layout.addWidget(QLabel("Scripts Section"))

        self.script_editor = QTextEdit()
        layout.addWidget(self.script_editor)

        self.load_button = QPushButton("Load Script")
        self.load_button.clicked.connect(self.load_script)
        layout.addWidget(self.load_button)

        self.save_button = QPushButton("Save Script")
        self.save_button.clicked.connect(self.save_script)
        layout.addWidget(self.save_button)

        self.run_button = QPushButton("Run Script")
        self.run_button.clicked.connect(self.run_script)
        layout.addWidget(self.run_button)

        self.stop_button = QPushButton("Stop Script")
        self.stop_button.clicked.connect(self.stop_script)
        layout.addWidget(self.stop_button)

        self.record_button = QPushButton("Start Recording")
        self.record_button.clicked.connect(self.toggle_recording)
        layout.addWidget(self.record_button)

        self.record_delay_checkbox = QCheckBox("Record Delay")
        self.record_delay_checkbox.setChecked(True)
        layout.addWidget(self.record_delay_checkbox)

        self.interval_layout = QHBoxLayout()
        layout.addWidget(QLabel("Interval between actions:"))
        self.hours_input = QSpinBox(self)
        self.hours_input.setRange(0, 23)
        self.minutes_input = QSpinBox(self)
        self.minutes_input.setRange(0, 59)
        self.seconds_input = QSpinBox(self)
        self.seconds_input.setRange(0, 59)
        self.milliseconds_input = QSpinBox(self)
        self.milliseconds_input.setRange(0, 999)
        self.interval_layout.addWidget(QLabel("Hours"))
        self.interval_layout.addWidget(self.hours_input)
        self.interval_layout.addWidget(QLabel("Minutes"))
        self.interval_layout.addWidget(self.minutes_input)
        self.interval_layout.addWidget(QLabel("Seconds"))
        self.interval_layout.addWidget(self.seconds_input)
        self.interval_layout.addWidget(QLabel("Milliseconds"))
        self.interval_layout.addWidget(self.milliseconds_input)
        layout.addLayout(self.interval_layout)

        self.run_mode_combo = QComboBox()
        self.run_mode_combo.addItems(["Infinite (Until Stopped)", "X times"])
        layout.addWidget(QLabel("Run Mode:"))
        layout.addWidget(self.run_mode_combo)

        self.run_times_input = QSpinBox(self)
        self.run_times_input.setMinimum(1)
        self.run_times_input.setMaximum(1000000)
        self.run_times_input.setValue(1)
        layout.addWidget(self.run_times_input)

        self.setLayout(layout)

    def load_script(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Script", "",
                                                   "AHK Scripts (*.ahk);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as file:
                self.script_editor.setPlainText(file.read())

    def save_script(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Script", "",
                                                   "AHK Scripts (*.ahk);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as file:
                file.write(self.script_editor.toPlainText())

    def run_script(self):
        script_content = self.script_editor.toPlainText()
        if not script_content.strip():
            QMessageBox.warning(self, "Warning", "Script content is empty.")
            return

        self.temp_script_file = "temp_script.ahk"
        with open(self.temp_script_file, 'w') as file:
            file.write(script_content)

        try:
            self.process = subprocess.Popen(["autohotkey", self.temp_script_file])
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"Failed to run script: {e}")

    def stop_script(self):
        if self.process:
            self.process.terminate()
            self.process = None
            QMessageBox.information(self, "Info", "Script stopped.")
        else:
            QMessageBox.warning(self, "Warning", "No script is running.")

    def toggle_recording(self):
        if self.listener is None:
            self.start_recording()
            self.record_button.setText("Stop Recording")
        else:
            self.stop_recording()
            self.record_button.setText("Start Recording")

    def start_recording(self):
        self.listener = Listener(self.script_editor, self.record_delay_checkbox.isChecked())
        self.listener.signal_emitter = self.signal_emitter
        self.listener.start()

    def stop_recording(self):
        if self.listener:
            self.listener.stop()
            self.listener = None

    def update_script_editor(self, text):
        self.script_editor.append(text)
    
    def get_settings(self):
        return {
            'script_content': self.script_editor.toPlainText(),
            'record_delay': self.record_delay_checkbox.isChecked(),
            'interval': self.get_interval(),
            'run_mode': self.run_mode_combo.currentText(),
            'run_times': self.run_times_input.value(),
        }

    def updateSettings(self, settings):
        self.script_editor.setPlainText(settings['script_content'])
        self.record_delay_checkbox.setChecked(settings['record_delay'])
        interval = settings['interval']
        self.hours_input.setValue(interval // 3600)
        self.minutes_input.setValue((interval % 3600) // 60)
        self.seconds_input.setValue(interval % 60)
        self.milliseconds_input.setValue(int((interval * 1000) % 1000))
        self.run_mode_combo.setCurrentText(settings['run_mode'])
        self.run_times_input.setValue(settings['run_times'])

    def get_default_settings(self):
        return {
            'script_content': '',
            'record_delay': True,
            'interval': 1.0,
            'run_mode': 'Infinite (Until Stopped)',
            'run_times': 1,
        }

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
            self.signal_emitter.text_signal.emit(f"Sleep, {int(delay * 1000)}\n")

    def on_press(self, key):
        self.record_delay_func()
        try:
            key_str = key.char
        except AttributeError:
            key_str = key.name
        if self.signal_emitter:
            self.signal_emitter.text_signal.emit(f"Send, {{{key_str}}}\n")

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.record_delay_func()
            if self.signal_emitter:
                self.signal_emitter.text_signal.emit(f"Click, {x}, {y}\n")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Scripts()
    ex.resize(400, 500)
    ex.show()
    sys.exit(app.exec_())
