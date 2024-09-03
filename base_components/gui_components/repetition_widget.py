
from PyQt5.QtWidgets import QVBoxLayout, QSpinBox, QGroupBox, QRadioButton
from PyQt5.QtCore import pyqtSignal

class RepeatActionWidget(QGroupBox):
    change_settings = pyqtSignal(dict)
    def __init__(self):
        super().__init__("Number of Actions")
        press_times_layout = QVBoxLayout()
        
        self.repeat_until_stopped_radio = QRadioButton("Repeat Until Stopped")
        self.repeat_until_stopped_radio.setChecked(True)
        self.repeat_until_stopped_radio.clicked.connect(
            lambda: self.change_settings.emit({'repeat_inf': True})
        )
        self.repeat_radio = QRadioButton("Repeat 'X' times")
        self.repeat_radio.clicked.connect(
            lambda: self.change_settings.emit({'repeat_inf': False})
        )
        press_times_layout.addWidget(self.repeat_until_stopped_radio)
        press_times_layout.addWidget(self.repeat_radio)
        self.press_times_input = QSpinBox(self)
        self.press_times_input.setMinimum(1)
        self.press_times_input.setMaximum(1000000)
        self.press_times_input.setValue(1)
        self.press_times_input.valueChanged.connect(
            lambda: self.change_settings.emit({'repeat_times': self.press_times_input.value()})
        )
        press_times_layout.addWidget(self.press_times_input)
        self.setLayout(press_times_layout)


