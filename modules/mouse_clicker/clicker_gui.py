from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from base_components.base_gui import BaseAutoActionGUI
from PyQt5.QtCore import Qt
from modules.mouse_clicker.click_position_widget import ClickPositionWidget
from modules.mouse_clicker.button_action_widget import ButtonActionWidget

class ClickerGUI(BaseAutoActionGUI):
    def __init__(self):
        super().__init__("Auto Mouse Clicker")
        self.initClickerUI()

    def initClickerUI(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        main_layout.addWidget(self.title_widget)

        temporary_horizontal_layout = QHBoxLayout()

        self.button_action_widget = ButtonActionWidget()
        self.button_action_widget.change_settings.connect(self.changeSettings.emit)
    
        temporary_horizontal_layout.addWidget(self.button_action_widget)
        temporary_horizontal_layout.addWidget(self.repeat_action_widget)

        main_layout.addLayout(temporary_horizontal_layout)

        main_layout.addWidget(self.interval_widget)

        self.position_group = ClickPositionWidget()
        self.position_group.change_settings.connect(self.changeSettings.emit)
        main_layout.addWidget(self.position_group)

        main_layout.addWidget(self.sound_effect_checkbox)

        main_layout.addWidget(self.start_stop_widget)

        self.setLayout(main_layout)

    def update_settings(self, new_settings: dict):
        super().update_settings(new_settings)
        if new_settings.get('button', None):
            self.button_action_widget.button_combo.setCurrentText(new_settings['button'])
        if new_settings.get('action', None):
            self.button_action_widget.action_combo.setCurrentText(new_settings['action'])
        if new_settings.get('position_mode', None):
            self.position_group.position_combo_widget.combo.setCurrentText(new_settings['position_mode'])
        if new_settings.get('x_pos', None) and new_settings.get('y_pos', None):
            self.position_group.coord_input_widget.x_input.setText(new_settings['x_pos'])
            self.position_group.coord_input_widget.y_input.setText(new_settings['y_pos'])
        if new_settings.get('top_left_x_pos', None) and new_settings.get('top_left_y_pos', None) and new_settings.get('bottom_right_x_pos', None) and new_settings.get('bottom_right_y_pos', None):
            self.position_group.rectangle_input_widget.top_left_x.setText(new_settings['top_left_x_pos'])
            self.position_group.rectangle_input_widget.top_left_y.setText(new_settings['top_left_y_pos'])
            self.position_group.rectangle_input_widget.bottom_right_x.setText(new_settings['bottom_right_x_pos'])
            self.position_group.rectangle_input_widget.bottom_right_y.setText(new_settings['bottom_right_y_pos'])
            

