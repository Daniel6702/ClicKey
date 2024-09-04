from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QTextEdit, QCheckBox, QHBoxLayout
from base_components.base_gui import BaseAutoActionGUI
from PyQt5.QtCore import Qt, pyqtSignal

class ScriptGUI(BaseAutoActionGUI):
    start_recording_signal = pyqtSignal()
    stop_recording_signal = pyqtSignal()
    save_script_signal = pyqtSignal(str)
    load_script_signal = pyqtSignal()

    def __init__(self):
        super().__init__("Script Runner")
        self.initScriptUI()

    def initScriptUI(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        main_layout.addWidget(self.title_widget)

        # Script Editor
        self.script_editor = QTextEdit(self)
        self.old_text = ""
        self.script_editor.textChanged.connect(self.script_editor_text_changed)
        self.script_editor.setPlaceholderText("Script will be displayed here...")
        main_layout.addWidget(self.script_editor)

        # Toggle recording delay checkbox
        self.record_delay_checkbox = QCheckBox("Record delay between actions")
        self.record_delay_checkbox.stateChanged.connect(lambda: self.changeSettings.emit({'delay': self.record_delay_checkbox.isChecked()}))
        main_layout.addWidget(self.record_delay_checkbox)

        # Recording buttons
        button_layout = QHBoxLayout()

        self.record_button = QPushButton("Start Recording")
        self.record_button.setCheckable(True)
        self.record_button.toggled.connect(self.toggle_recording)
        button_layout.addWidget(self.record_button)

        self.save_button = QPushButton("Save Script")
        self.save_button.clicked.connect(self.save_script)
        button_layout.addWidget(self.save_button)

        self.load_button = QPushButton("Load Script")
        self.load_button.clicked.connect(self.load_script)
        button_layout.addWidget(self.load_button)

        main_layout.addLayout(button_layout)

        main_layout.addWidget(self.interval_widget)

        main_layout.addWidget(self.sound_effect_checkbox)

        main_layout.addWidget(self.start_stop_widget)

        self.setLayout(main_layout)

    def script_editor_text_changed(self):
        # Get the current text
        new_text = self.script_editor.toPlainText()

        # Split the old and new text into lists of lines
        old_lines = self.old_text.split('\n')
        new_lines = new_text.split('\n')

        # Find which lines were changed by comparing the old and new text line by line
        changed_lines = []
        changed_text = []

        for i, (old_line, new_line) in enumerate(zip(old_lines, new_lines)):
            if old_line != new_line:
                changed_lines.append(i + 1)  # Line numbers are 1-indexed
                changed_text.append(new_line)  # Append the updated line

        # If new lines were added, we track those separately
        if len(new_lines) > len(old_lines):
            for i in range(len(old_lines), len(new_lines)):
                changed_lines.append(i + 1)  # The new lines start after the old lines
                changed_text.append(new_lines[i])

        # Emit the custom signal with the updated line text and the line numbers
        if len(changed_lines) > 0 and len(changed_text) > 0:
            self.changeSettings.emit({
                'script_edit': changed_text[0],  # List of changed lines
                'changed_lines': changed_lines[0]-1  # Line numbers that were changed
            })

        # Update old_text to the current text
        self.old_text = new_text

    def toggle_recording(self, is_recording):
        if is_recording:
            self.record_button.setText("Stop Recording")
            self.script_editor.setText("")
            self.script_editor.setReadOnly(True)
            self.start_recording_signal.emit()
        else:
            self.record_button.setText("Start Recording")
            self.stop_recording_signal.emit()
            self.script_editor.setReadOnly(False)
            

    def save_script(self):
        script = self.script_editor.toPlainText()
        self.save_script_signal.emit(script)

    def load_script(self):
        self.load_script_signal.emit()

    def update_script_display(self, action: dict):
        self.script_editor.append(str(action))

    def update_gui(self, load_script=False, script=""):
        if load_script:
            self.update_script_display(script)
        else:
            super().update_gui()

