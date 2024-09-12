from base_components.base_gui import BaseGUI
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import pyqtSignal, Qt

class SettingsGUI(BaseGUI):
    def __init__(self):
        super().__init__("Settings")
        self.initClickerUI()

    def initClickerUI(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        self.title_widget.status_label.setText("Clickey is an open-source, Python-based automation utility tool that combines several modules, \n such as an Auto Mouse Clicker, Auto Key Presser, Script Runner, Color Tools, System Monitor, and more.")
        main_layout.addWidget(self.title_widget)

        self.setLayout(main_layout)