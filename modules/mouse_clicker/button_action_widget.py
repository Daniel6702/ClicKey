from PyQt5.QtWidgets import QVBoxLayout, QLabel, QComboBox, QGroupBox
from PyQt5.QtCore import pyqtSignal

class ButtonActionWidget(QGroupBox):
    change_settings = pyqtSignal(dict)
    def __init__(self):
        super().__init__("Click Action")
        button_action_layout = QVBoxLayout()

        self.button_combo = QComboBox(self)
        self.button_combo.addItems(["left", "right", "middle", "both"])
        self.button_combo.currentIndexChanged.connect(
            lambda: self.change_settings.emit({'button': self.button_combo.currentText()})
        )
        button_action_layout.addWidget(QLabel("Mouse Button"))
        button_action_layout.addWidget(self.button_combo)

        self.action_combo = QComboBox(self)
        self.action_combo.addItems(["single click", "double click"])
        self.action_combo.currentIndexChanged.connect(
            lambda: self.change_settings.emit({'action': self.action_combo.currentText().replace(' ', '_')})
        )
        button_action_layout.addWidget(QLabel("Action"))
        button_action_layout.addWidget(self.action_combo)
        self.setLayout(button_action_layout)
