from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit
from PyQt5.QtCore import  pyqtSignal

class KeyInputWidget(QWidget):
    change_settings = pyqtSignal(dict)
    def __init__(self) -> None:
        super().__init__()
        key_action_layout = QVBoxLayout()

        self.key_input = QLineEdit(self)
        self.key_input.setMaxLength(1)
        self.key_input.textChanged.connect(
            lambda: self.change_settings.emit({'key': self.key_input.text()})
        )
        key_action_layout.addWidget(QLabel("Key to Press"))
        key_action_layout.addWidget(self.key_input)
        self.setLayout(key_action_layout)