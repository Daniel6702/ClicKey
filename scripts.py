import sys
import subprocess
import os
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QTextEdit, QPushButton, QFileDialog, QApplication, QMessageBox)
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
        self.listener = Listener(self.script_editor)
        self.listener.signal_emitter = self.signal_emitter
        self.listener.start()

    def stop_recording(self):
        if self.listener:
            self.listener.stop()
            self.listener = None

    def update_script_editor(self, text):
        self.script_editor.append(text)

class Listener(threading.Thread):
    def __init__(self, editor):
        super().__init__()
        self.editor = editor
        self.running = True
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.signal_emitter = None

    def run(self):
        with self.keyboard_listener as kl, self.mouse_listener as ml:
            while self.running:
                kl.join(0.1)
                ml.join(0.1)

    def stop(self):
        self.running = False
        self.keyboard_listener.stop()
        self.mouse_listener.stop()

    def on_press(self, key):
        try:
            key_str = key.char
        except AttributeError:
            key_str = key.name
        if self.signal_emitter:
            self.signal_emitter.text_signal.emit(f"Send, {{{key_str}}}")

    def on_click(self, x, y, button, pressed):
        if pressed:
            if self.signal_emitter:
                self.signal_emitter.text_signal.emit(f"Click, {x}, {y}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Scripts()
    ex.resize(400, 500)
    ex.show()
    sys.exit(app.exec_())
