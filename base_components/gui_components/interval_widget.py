from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSpinBox,QStackedLayout, QGroupBox, QCheckBox
from PyQt5.QtCore import pyqtSignal

class IntervalWidget(QGroupBox):
    change_settings = pyqtSignal(dict)
    def __init__(self):
        super().__init__("Interval")
        interval_layout = QVBoxLayout()
        self.random_delay_checkbox = QCheckBox("Random interval")
        self.random_delay_checkbox.stateChanged.connect(self.random_delay_checkbox_changed)
        interval_layout.addWidget(self.random_delay_checkbox)
        self.interval_stacked_layout = QStackedLayout()
        self.random_interval_widget = QWidget()
        self.fixed_interval_widget = QWidget()
        fixed_interval_layout = QHBoxLayout(self.fixed_interval_widget)
        self.hours_input = QSpinBox(self)
        self.hours_input.setRange(0, 23)
        self.hours_input.valueChanged.connect(self.interval_changed)
        self.hours_label = QLabel("Hours")
        self.minutes_input = QSpinBox(self)
        self.minutes_input.setRange(0, 59)
        self.minutes_input.valueChanged.connect(self.interval_changed)
        self.minute_label = QLabel("Minutes")
        self.seconds_input = QSpinBox(self)
        self.seconds_input.setRange(0, 59)
        self.seconds_input.setValue(1)
        self.seconds_input.valueChanged.connect(self.interval_changed)
        self.seconds_label = QLabel("Seconds")
        self.milliseconds_input = QSpinBox(self)
        self.milliseconds_input.setRange(0, 999)
        self.milliseconds_input.valueChanged.connect(self.interval_changed)
        self.milliseconds_label = QLabel("Milliseconds")
        fixed_interval_layout.addWidget(self.hours_label)
        fixed_interval_layout.addWidget(self.hours_input)
        fixed_interval_layout.addWidget(self.minute_label)
        fixed_interval_layout.addWidget(self.minutes_input)
        fixed_interval_layout.addWidget(self.seconds_label)
        fixed_interval_layout.addWidget(self.seconds_input)
        fixed_interval_layout.addWidget(self.milliseconds_label)
        fixed_interval_layout.addWidget(self.milliseconds_input)
        random_interval_layout = QHBoxLayout(self.random_interval_widget)
        self.min_delay_input = QSpinBox(self)
        self.min_delay_input.setRange(0, 3600)
        self.min_delay_input.valueChanged.connect(
            lambda: self.change_settings.emit({'min_delay': self.min_delay_input.value()}))
        self.max_delay_input = QSpinBox(self)
        self.max_delay_input.setRange(0, 3600)
        self.max_delay_input.valueChanged.connect(
            lambda: self.change_settings.emit({'max_delay': self.max_delay_input.value()}))
        random_interval_layout.addWidget(QLabel("Min delay (s)"))
        random_interval_layout.addWidget(self.min_delay_input)
        random_interval_layout.addWidget(QLabel("Max delay (s)"))
        random_interval_layout.addWidget(self.max_delay_input)
        self.interval_stacked_layout.addWidget(self.fixed_interval_widget)
        self.interval_stacked_layout.addWidget(self.random_interval_widget)
        interval_layout.addLayout(self.interval_stacked_layout)
        self.setLayout(interval_layout)

    def random_delay_checkbox_changed(self):
        self.interval_stacked_layout.setCurrentIndex(self.random_delay_checkbox.isChecked())
        self.change_settings.emit({'random_interval': self.random_delay_checkbox.isChecked()})

    def interval_changed(self):
        hours = self.hours_input.value()
        minutes = self.minutes_input.value()
        seconds = self.seconds_input.value()
        milliseconds = self.milliseconds_input.value()
        total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000.0
        self.change_settings.emit({'interval_norm': total_seconds})