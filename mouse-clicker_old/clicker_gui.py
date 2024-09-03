from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QSpinBox, QLineEdit, QPushButton, QHBoxLayout, QCheckBox, QGroupBox, QStackedLayout, QRadioButton
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
import pyautogui

class ClickerGUI(QWidget):
    changeSettings = pyqtSignal(dict, name='changeSettings')
    changeStatus = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.initUI()
        self.update_position_fields(0)

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        self.title = QLabel("Auto Mouse Clicker")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title)

        self.status_label = QLabel("Status: Idle")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)

        # Group Box for Mouse Button and Action
        button_action_group = QGroupBox("Click Action")
        button_action_layout = QVBoxLayout()
        button_action_group.setLayout(button_action_layout)

        self.button_combo = QComboBox(self)
        self.button_combo.addItems(["left", "right", "middle", "both"])
        self.button_combo.currentIndexChanged.connect(
            lambda: self.changeSettings.emit({'button': self.button_combo.currentText()})
        )
        button_action_layout.addWidget(QLabel("Mouse Button"))
        button_action_layout.addWidget(self.button_combo)

        self.action_combo = QComboBox(self)
        self.action_combo.addItems(["single click", "double click"])
        self.action_combo.currentIndexChanged.connect(
            lambda: self.changeSettings.emit({'action': self.action_combo.currentText().replace(' ', '_')})
        )
        button_action_layout.addWidget(QLabel("Action"))
        button_action_layout.addWidget(self.action_combo)

        # Group Box for Number of Clicks
        click_times_group = QGroupBox("Number of Clicks")
        click_times_layout = QVBoxLayout()
        click_times_group.setLayout(click_times_layout)

        self.repeat_until_stopped_radio = QRadioButton("Repeat Until Stopped")
        self.repeat_until_stopped_radio.setChecked(True)
        self.repeat_until_stopped_radio.clicked.connect(
            lambda: self.changeSettings.emit({'click_inf': True})
        )
        self.repeat_radio = QRadioButton("Repeat 'X' times")
        self.repeat_radio.clicked.connect(
            lambda: self.changeSettings.emit({'click_inf': False})
        )
        click_times_layout.addWidget(self.repeat_until_stopped_radio)
        click_times_layout.addWidget(self.repeat_radio)

        self.click_times_input = QSpinBox(self)
        self.click_times_input.setMinimum(1)
        self.click_times_input.setMaximum(1000000)
        self.click_times_input.setValue(1)
        self.click_times_input.valueChanged.connect(
            lambda: self.changeSettings.emit({'click_times': self.click_times_input.value()})
        )
        click_times_layout.addWidget(self.click_times_input)

        temp = QHBoxLayout()
        temp.addWidget(button_action_group)
        temp.addWidget(click_times_group)
        main_layout.addLayout(temp)

        # Group Box for Click Interval
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

        # Group Box for Click Position
        self.position_group = QGroupBox("Click Position")
        self.position_group.setMinimumWidth(505)
        position_layout = QVBoxLayout()
        self.position_group.setLayout(position_layout)

        temp = QHBoxLayout()
        self.mouse_position_label = QLabel("Current Mouse Position:\n (X: 0, Y: 0)")
        self.mouse_position_label.setStyleSheet("font-size: 12px; color: #555; margin-left: 45px;")
        self.position_combo = QComboBox(self)
        self.position_combo.addItems(["follow mouse", "center", "coordinates", "random position", "rectangle"])
        self.position_combo.currentIndexChanged.connect(self.update_position_fields)
        position_layout.addWidget(QLabel("Click Position:"))
        temp.addWidget(self.position_combo)
        temp.addWidget(self.mouse_position_label)

        position_layout.addLayout(temp)

        self.coord_widget = QWidget()
        self.coord_h_layout = QHBoxLayout()
        self.coord_v_layout_left = QVBoxLayout()
        self.coord_v_layout_right = QVBoxLayout()
        self.coord_x_input = QLineEdit(self)
        self.coord_x_input.textChanged.connect(
            lambda: self.changeSettings.emit({'x_pos': int(self.coord_x_input.text())})
        )
        self.coord_y_input = QLineEdit(self)
        self.coord_y_input.textChanged.connect(
            lambda: self.changeSettings.emit({'y_pos': int(self.coord_y_input.text())})
        )
        self.coord_x_label = QLabel("X Coordinate:")
        self.coord_y_label = QLabel("Y Coordinate:")

        self.coord_v_layout_left.addWidget(self.coord_x_label)
        self.coord_v_layout_left.addWidget(self.coord_y_label)
        self.coord_v_layout_right.addWidget(self.coord_x_input)
        self.coord_v_layout_right.addWidget(self.coord_y_input)
        self.coord_h_layout.addLayout(self.coord_v_layout_left)
        self.coord_h_layout.addLayout(self.coord_v_layout_right)
        self.coord_widget.setLayout(self.coord_h_layout)
        position_layout.addWidget(self.coord_widget)

        self.rectangle_layout = QVBoxLayout()

        # Create horizontal layouts for top-left and bottom-right coordinates
        self.top_left_layout = QHBoxLayout()
        self.bottom_right_layout = QHBoxLayout()

        # Line edits and labels for top-left coordinates
        self.rectangle_top_left_x = QLineEdit(self)
        self.rectangle_top_left_y = QLineEdit(self)
        self.rectangle_top_left_x.textChanged.connect(
            lambda: self.changeSettings.emit({'top_left_x_pos': int(self.rectangle_top_left_x.text())})
        )
        self.rectangle_top_left_y.textChanged.connect(
            lambda: self.changeSettings.emit({'top_left_y_pos': int(self.rectangle_top_left_y.text())})
        )
        self.top_left_x_label = QLabel("Top Left X:")
        self.top_left_y_label = QLabel("Top Left Y:")

        # Adding widgets to the top-left layout
        self.top_left_layout.addWidget(self.top_left_x_label)
        self.top_left_layout.addWidget(self.rectangle_top_left_x)
        self.top_left_layout.addWidget(self.top_left_y_label)
        self.top_left_layout.addWidget(self.rectangle_top_left_y)

        # Line edits and labels for bottom-right coordinates
        self.rectangle_bottom_right_x = QLineEdit(self)
        self.rectangle_bottom_right_y = QLineEdit(self)
        self.rectangle_bottom_right_x.textChanged.connect(
            lambda: self.changeSettings.emit({'bottom_right_x_pos': int(self.rectangle_bottom_right_x.text())})
        )
        self.rectangle_bottom_right_y.textChanged.connect(
            lambda: self.changeSettings.emit({'bottom_right_y_pos': int(self.rectangle_bottom_right_y.text())})
        )
        self.bottom_right_x_label = QLabel("Bottom Right X:")
        self.bottom_right_y_label = QLabel("Bottom Right Y:")

        # Adding widgets to the bottom-right layout
        self.bottom_right_layout.addWidget(self.bottom_right_x_label)
        self.bottom_right_layout.addWidget(self.rectangle_bottom_right_x)
        self.bottom_right_layout.addWidget(self.bottom_right_y_label)
        self.bottom_right_layout.addWidget(self.rectangle_bottom_right_y)

        # Adding top-left and bottom-right layouts to the main layout
        self.rectangle_layout.addLayout(self.top_left_layout)
        self.rectangle_layout.addLayout(self.bottom_right_layout)
        self.rectangle_widget = QWidget()
        self.rectangle_widget.setLayout(self.rectangle_layout)

        # Add the overall layout to the parent layout
        position_layout.addWidget(self.rectangle_widget)

        main_layout.addWidget(self.position_group)

        # Sound Effect Option
        self.sound_effect_checkbox = QCheckBox("Sound effect on click")
        self.sound_effect_checkbox.stateChanged.connect(
            lambda: self.changeSettings.emit({'sound_effect': self.sound_effect_checkbox.isChecked()})
        )
        main_layout.addWidget(self.sound_effect_checkbox)

        # Start and Stop Buttons
        self.start_stop_layout = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.start_button.setObjectName("startButton")
        self.start_button.setCheckable(True)
        self.start_button.clicked.connect(self.start_clicker)
        self.start_stop_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setObjectName("stopButton")
        self.stop_button.clicked.connect(self.stop_clicker)
        self.start_stop_layout.addWidget(self.stop_button)

        main_layout.addLayout(self.start_stop_layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_mouse_position)
        self.timer.start(100)

        self.setLayout(main_layout)

    def random_delay_checkbox_changed(self):
        self.interval_stacked_layout.setCurrentIndex(self.random_delay_checkbox.isChecked())
        self.changeSettings.emit({'random_interval': self.random_delay_checkbox.isChecked()})

    def update_mouse_position(self):
        x,y = pyautogui.position()
        self.mouse_position_label.setText(f"Current Mouse Position:\n (X: {x}, Y: {y})")
    
    def update_position_fields(self, index):
        self.changeSettings.emit({'position_mode': self.position_combo.currentText().replace(' ', '_')})
        self.coord_widget.setVisible(False)
        self.rectangle_widget.setVisible(False)
        if index == 2:  
            self.coord_widget.setVisible(True)            
        elif index == 4:  
            self.rectangle_widget.setVisible(True)

    def start_clicker(self):
        self.start_button.setEnabled(False)  
        self.changeStatus.emit(True)
        self.status_label.setText("Status: Running")

    def stop_clicker(self):
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