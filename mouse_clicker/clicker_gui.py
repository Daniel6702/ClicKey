from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from base_components.base_gui import BaseAutoActionGUI
from PyQt5.QtCore import Qt
from mouse_clicker.click_position_widget import ClickPositionWidget
from mouse_clicker.button_action_widget import ButtonActionWidget

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

    

