from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QTextEdit, QCheckBox, QHBoxLayout
from base_components.base_gui import BaseGUI
from PyQt5.QtCore import Qt, pyqtSignal

class NoSelectionTextEdit(QTextEdit):
    def __init__(self, *args, **kwargs):
        super(NoSelectionTextEdit, self).__init__(*args, **kwargs)
    
    def mouseMoveEvent(self, event):
        pass

class ScriptGUI(BaseGUI):
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
        self.script_editor = NoSelectionTextEdit(self)
        
        self.old_text = ""
        self.script_editor.textChanged.connect(lambda: self.changeSettings.emit({'script_edit': self.script_editor.toPlainText()}))
        self.script_editor.setPlaceholderText("Script will be displayed here...")
        main_layout.addWidget(self.script_editor)

        # Toggle recording delay checkbox
        temp_H = QHBoxLayout()

        self.record_delay_checkbox = QCheckBox("Record delay between actions")
        self.record_delay_checkbox.stateChanged.connect(lambda: self.changeSettings.emit({'delay': self.record_delay_checkbox.isChecked()}))
        temp_H.addWidget(self.record_delay_checkbox)

        self.record_mouse_position_checkbox = QCheckBox("Record mouse position")
        self.record_mouse_position_checkbox.stateChanged.connect(lambda: self.changeSettings.emit({'position': self.record_mouse_position_checkbox.isChecked()}))
        temp_H.addWidget(self.record_mouse_position_checkbox)

        main_layout.addLayout(temp_H)

        # Recording buttons
        button_layout = QHBoxLayout()

        self.record_button = QPushButton("Start Recording")
        self.record_button.setCheckable(True)
        self.record_button.toggled.connect(self.toggle_recording)
        button_layout.addWidget(self.record_button)

        self.save_button = QPushButton("Save Script")
        self.save_button.clicked.connect(lambda: self.save_script_signal.emit(self.script_editor.toPlainText()))
        button_layout.addWidget(self.save_button)

        self.load_button = QPushButton("Load Script")
        self.load_button.clicked.connect(lambda: self.load_script_signal.emit())
        button_layout.addWidget(self.load_button)

        main_layout.addLayout(button_layout)

        temp_H = QHBoxLayout()

        temp_H.addWidget(self.repeat_action_widget)

        temp_H.addWidget(self.interval_widget)

        main_layout.addLayout(temp_H)

        main_layout.addWidget(self.sound_effect_checkbox)

        main_layout.addWidget(self.start_stop_widget)

        self.setLayout(main_layout)

    def toggle_recording(self, is_recording):
        if is_recording:
            self.record_button.setText("Stop Recording")
            self.script_editor.setReadOnly(True)
            self.start_recording_signal.emit()
        else:
            self.record_button.setText("Start Recording")
            self.stop_recording_signal.emit()
            self.script_editor.setReadOnly(False)

    def toggle_recording_button(self):
        if self.record_button.text() == "Start Recording":
            self.toggle_recording(True)
        else:
            self.toggle_recording(False)

    def update_script(self, script=""):
        print(f"Updating script: {script}")
        self.script_editor.append(str(script))

    def update_settings(self, new_settings: dict):
        super().update_settings(new_settings)
        if new_settings.get('delay', None):
            self.record_delay_checkbox.setChecked(new_settings['delay'])
        if new_settings.get('position', None):
            self.record_mouse_position_checkbox.setChecked(new_settings['position'])