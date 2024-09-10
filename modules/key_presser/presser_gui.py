from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGroupBox
from base_components.base_gui import BaseAutoActionGUI
from PyQt5.QtCore import Qt
from modules.key_presser.combo_box_widget import ComboBoxWidget
from modules.key_presser.key_input_widget import KeyInputWidget

class KeyPresserGUI(BaseAutoActionGUI):
    def __init__(self):
        super().__init__("Auto Key Presser")
        self.initKeyPresserUI()

    def initKeyPresserUI(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        main_layout.addWidget(self.title_widget)

        # Group Box for Key and Modifiers
        key_action_group = QGroupBox("Key Action")
        key_action_layout = QVBoxLayout()
        key_action_group.setLayout(key_action_layout)

        self.key_input_widget = KeyInputWidget()
        self.key_input_widget.change_settings.connect(self.changeSettings.emit)
        key_action_layout.addWidget(self.key_input_widget)

        self.combo_widget = ComboBoxWidget()
        self.combo_widget.change_settings.connect(self.changeSettings.emit)
        key_action_layout.addWidget(self.combo_widget)

        temporary_horizontal_layout = QHBoxLayout()
        temporary_horizontal_layout.addWidget(key_action_group)

        # Group Box for Number of Presses
        temporary_horizontal_layout.addWidget(self.repeat_action_widget)

        main_layout.addLayout(temporary_horizontal_layout)

        # Interval Option
        main_layout.addWidget(self.interval_widget)

        # Sound Effect Option
        main_layout.addWidget(self.sound_effect_checkbox)

        # Start/Stop Button
        main_layout.addWidget(self.start_stop_widget)

        self.setLayout(main_layout)

    def update_settings(self, new_settings: dict):
        super().update_settings(new_settings)
        if new_settings.get('key', None):
            self.key_input_widget.key_input.setText(new_settings['key'])
        if new_settings.get('ctrl', None):
            self.combo_widget.ctrl_checkbox.setChecked(new_settings['ctrl'])
        if new_settings.get('alt', None):
            self.combo_widget.alt_checkbox.setChecked(new_settings['alt'])
        if new_settings.get('shift', None):
            self.combo_widget.shift_checkbox.setChecked(new_settings['shift'])