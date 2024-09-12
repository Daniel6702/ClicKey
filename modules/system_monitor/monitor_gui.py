from base_components.base_gui import BaseGUI
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import pyqtSignal, Qt

class MonitorGUI(BaseGUI):
    def __init__(self):
        super().__init__("System Monitor")
        self.initClickerUI()

    def initClickerUI(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        self.title_widget.status_label.setText("")
        main_layout.addWidget(self.title_widget)

        self.setLayout(main_layout)