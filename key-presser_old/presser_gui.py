from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpinBox, QLineEdit, QPushButton, QHBoxLayout, QCheckBox, QGroupBox, QStackedLayout, QRadioButton
from PyQt5.QtCore import Qt, pyqtSignal

class KeyPresserGUI(QWidget):
    changeSettings = pyqtSignal(dict, name='changeSettings')
    changeStatus = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        self.title = QLabel("Auto Key Presser")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title)

        self.status_label = QLabel("Status: Idle")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)

        # Group Box for Key and Modifiers
        key_action_group = QGroupBox("Key Action")
        key_action_layout = QVBoxLayout()
        key_action_group.setLayout(key_action_layout)

        self.key_input = QLineEdit(self)
        self.key_input.setMaxLength(1)  # Only accept a single character
        self.key_input.textChanged.connect(
            lambda: self.changeSettings.emit({'key': self.key_input.text()})
        )
        key_action_layout.addWidget(QLabel("Key to Press"))
        key_action_layout.addWidget(self.key_input)

        self.ctrl_checkbox = QCheckBox("Ctrl")
        self.ctrl_checkbox.stateChanged.connect(
            lambda: self.changeSettings.emit({'ctrl': self.ctrl_checkbox.isChecked()})
        )
        self.alt_checkbox = QCheckBox("Alt")
        self.alt_checkbox.stateChanged.connect(
            lambda: self.changeSettings.emit({'alt': self.alt_checkbox.isChecked()})
        )
        self.shift_checkbox = QCheckBox("Shift")
        self.shift_checkbox.stateChanged.connect(
            lambda: self.changeSettings.emit({'shift': self.shift_checkbox.isChecked()})
        )
        key_action_layout.addWidget(self.ctrl_checkbox)
        key_action_layout.addWidget(self.alt_checkbox)
        key_action_layout.addWidget(self.shift_checkbox)

        # Group Box for Number of Presses
        press_times_group = QGroupBox("Number of Presses")
        press_times_layout = QVBoxLayout()
        press_times_group.setLayout(press_times_layout)

        self.repeat_until_stopped_radio = QRadioButton("Repeat Until Stopped")
        self.repeat_until_stopped_radio.setChecked(True)
        self.repeat_until_stopped_radio.clicked.connect(
            lambda: self.changeSettings.emit({'repeat_inf': True})
        )
        self.repeat_radio = QRadioButton("Repeat 'X' times")
        self.repeat_radio.clicked.connect(
            lambda: self.changeSettings.emit({'repeat_inf': False})
        )
        press_times_layout.addWidget(self.repeat_until_stopped_radio)
        press_times_layout.addWidget(self.repeat_radio)

        self.press_times_input = QSpinBox(self)
        self.press_times_input.setMinimum(1)
        self.press_times_input.setMaximum(1000000)
        self.press_times_input.setValue(1)
        self.press_times_input.valueChanged.connect(
            lambda: self.changeSettings.emit({'repeat_times': self.press_times_input.value()})
        )
        press_times_layout.addWidget(self.press_times_input)

        temp = QHBoxLayout()
        temp.addWidget(key_action_group)
        temp.addWidget(press_times_group)
        main_layout.addLayout(temp)

        # Group Box for Key Press Interval
        self.interval_group = QGroupBox("Interval")
        interval_layout = QVBoxLayout()
        self.interval_group.setLayout(interval_layout)

        self.random_delay_checkbox = QCheckBox("Random interval")
        self.random_delay_checkbox.stateChanged.connect(self.random_delay_checkbox_changed)
        interval_layout.addWidget(self.random_delay_checkbox)

        # Create stacked layout for fixed and random interval inputs
        self.interval_stacked_layout = QStackedLayout()
        self.fixed_interval_widget = QWidget()
        self.random_interval_widget = QWidget()

        # Fixed interval layout
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

        # Random interval layout
        random_interval_layout = QHBoxLayout(self.random_interval_widget)
        self.min_delay_input = QSpinBox(self)
        self.min_delay_input.setRange(0, 3600)
        self.min_delay_input.valueChanged.connect(
            lambda: self.changeSettings.emit({'min_delay': self.min_delay_input.value()})
        )
        self.max_delay_input = QSpinBox(self)
        self.max_delay_input.setRange(0, 3600)
        self.max_delay_input.valueChanged.connect(
            lambda: self.changeSettings.emit({'max_delay': self.max_delay_input.value()})
        )
        random_interval_layout.addWidget(QLabel("Min delay (s)"))
        random_interval_layout.addWidget(self.min_delay_input)
        random_interval_layout.addWidget(QLabel("Max delay (s)"))
        random_interval_layout.addWidget(self.max_delay_input)

        self.interval_stacked_layout.addWidget(self.fixed_interval_widget)
        self.interval_stacked_layout.addWidget(self.random_interval_widget)
        interval_layout.addLayout(self.interval_stacked_layout)

        main_layout.addWidget(self.interval_group)

        # Sound Effect Option
        self.sound_effect_checkbox = QCheckBox("Sound effect on key press")
        self.sound_effect_checkbox.stateChanged.connect(
            lambda: self.changeSettings.emit({'sound_effect': self.sound_effect_checkbox.isChecked()})
        )
        main_layout.addWidget(self.sound_effect_checkbox)

        # Start and Stop Buttons
        self.start_stop_layout = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.start_button.setObjectName("startButton")
        self.start_button.setCheckable(True)
        self.start_button.clicked.connect(self.start_key_presser)
        self.start_stop_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setObjectName("stopButton")
        self.stop_button.clicked.connect(self.stop_key_presser)
        self.start_stop_layout.addWidget(self.stop_button)

        main_layout.addLayout(self.start_stop_layout)

        self.setLayout(main_layout)

    def random_delay_checkbox_changed(self):
        self.interval_stacked_layout.setCurrentIndex(self.random_delay_checkbox.isChecked())
        self.changeSettings.emit({'random_interval': self.random_delay_checkbox.isChecked()})

    def start_key_presser(self):
        self.start_button.setEnabled(False)  
        self.changeStatus.emit(True)
        self.status_label.setText("Status: Running")

    def stop_key_presser(self):
        self.start_button.setEnabled(True)  
        self.changeStatus.emit(False)
        self.start_button.setChecked(False)
        self.status_label.setText("Status: Idle")

    def update_GUI(self):
        print("Updating GUI")
        self.start_button.setChecked(False)
        self.start_button.setEnabled(True)  

    def interval_changed(self):
        hours = self.hours_input.value()
        minutes = self.minutes_input.value()
        seconds = self.seconds_input.value()
        milliseconds = self.milliseconds_input.value()
        total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000.0
        self.changeSettings.emit({'interval_norm': total_seconds})
