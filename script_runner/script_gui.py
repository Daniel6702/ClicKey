from PyQt5.QtWidgets import QVBoxLayout
from base_components.base_gui import BaseAutoActionGUI
from PyQt5.QtCore import Qt

class ScriptGUI(BaseAutoActionGUI):
    def __init__(self):
        super().__init__("Script Runner")
        self.initScriptUI()

    def initScriptUI(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        main_layout.addWidget(self.title_widget)

        #Add it here

        main_layout.addWidget(self.interval_widget)

        main_layout.addWidget(self.sound_effect_checkbox)

        main_layout.addWidget(self.start_stop_widget)

        self.setLayout(main_layout)
