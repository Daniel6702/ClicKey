from PyQt5.QtWidgets import QWidget, QHBoxLayout, QCheckBox
from PyQt5.QtCore import pyqtSignal

class ComboBoxWidget(QWidget):
    change_settings = pyqtSignal(dict)
    def __init__(self) -> None:
        super().__init__()
        self.combo_layout = QHBoxLayout()
        self.ctrl_checkbox = QCheckBox("Ctrl")
        self.ctrl_checkbox.stateChanged.connect(
            lambda: self.change_settings.emit({'ctrl': self.ctrl_checkbox.isChecked()})
        )
        self.alt_checkbox = QCheckBox("Alt")
        self.alt_checkbox.stateChanged.connect(
            lambda: self.change_settings.emit({'alt': self.alt_checkbox.isChecked()})
        )
        self.shift_checkbox = QCheckBox("Shift")
        self.shift_checkbox.stateChanged.connect(
            lambda: self.change_settings.emit({'shift': self.shift_checkbox.isChecked()})
        )
        self.combo_layout.addWidget(self.ctrl_checkbox)
        self.combo_layout.addWidget(self.alt_checkbox)
        self.combo_layout.addWidget(self.shift_checkbox)
        self.setLayout(self.combo_layout)