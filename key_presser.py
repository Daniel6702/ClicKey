import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QSpinBox, QCheckBox, QPushButton, QHBoxLayout, QComboBox, QApplication, QGroupBox, QRadioButton, QStackedLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut
import random
import threading
import time

class KeyPresser(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.is_running = False
        self.thread = None

    def updateSettings(self, settings):
        self.start_hotkey = settings['start_key_presser_hotkey']
        self.stop_hotkey = settings['stop_key_presser_hotkey']
        self.initShortcuts()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        self.title = QLabel("Auto Key Presser")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title)

        # Group Box for Key and Action
        key_action_group = QGroupBox("Key Action")
        key_action_layout = QVBoxLayout()
        key_action_group.setLayout(key_action_layout)

        self.key_input = QLineEdit(self)
        key_action_layout.addWidget(QLabel("Key:"))
        key_action_layout.addWidget(self.key_input)

        self.hold_key_checkbox = QCheckBox("Hold key pressed between presses")
        key_action_layout.addWidget(self.hold_key_checkbox)

        self.continuous_hold_checkbox = QCheckBox("Continuously hold key pressed")
        key_action_layout.addWidget(self.continuous_hold_checkbox)

        # Group Box for Number of Presses
        press_times_group = QGroupBox("Number of Presses")
        press_times_layout = QVBoxLayout()
        press_times_group.setLayout(press_times_layout)

        self.repeat_until_stopped_radio = QRadioButton("Repeat Until Stopped")
        self.repeat_until_stopped_radio.setChecked(True)
        self.repeat_radio = QRadioButton("Repeat 'X' times")
        press_times_layout.addWidget(self.repeat_until_stopped_radio)
        press_times_layout.addWidget(self.repeat_radio)

        self.press_times_input = QSpinBox(self)
        self.press_times_input.setMinimum(1)
        self.press_times_input.setMaximum(1000000)
        self.press_times_input.setValue(1)
        press_times_layout.addWidget(self.press_times_input)

        temp = QHBoxLayout()
        temp.addWidget(key_action_group)
        temp.addWidget(press_times_group)
        main_layout.addLayout(temp)

        # Group Box for Press Interval
        self.interval_group = QGroupBox("Interval")
        interval_layout = QVBoxLayout()
        self.interval_group.setLayout(interval_layout)

        self.random_delay_checkbox = QCheckBox("Random interval")
        self.random_delay_checkbox.stateChanged.connect(self.update_random_delay_visibility)
        interval_layout.addWidget(self.random_delay_checkbox)

        # Create stacked layout for fixed and random interval inputs
        self.interval_stacked_layout = QStackedLayout()
        self.fixed_interval_widget = QWidget()
        self.random_interval_widget = QWidget()

        # Fixed interval layout
        fixed_interval_layout = QHBoxLayout(self.fixed_interval_widget)
        self.hours_input = QSpinBox(self)
        self.hours_input.setRange(0, 23)
        self.hours_label = QLabel("Hours")
        self.minutes_input = QSpinBox(self)
        self.minutes_input.setRange(0, 59)
        self.minute_label = QLabel("Minutes")
        self.seconds_input = QSpinBox(self)
        self.seconds_input.setRange(0, 59)
        self.seconds_label = QLabel("Seconds")
        self.milliseconds_input = QSpinBox(self)
        self.milliseconds_input.setRange(0, 999)
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
        self.max_delay_input = QSpinBox(self)
        self.max_delay_input.setRange(0, 3600)
        random_interval_layout.addWidget(QLabel("Min delay (s)"))
        random_interval_layout.addWidget(self.min_delay_input)
        random_interval_layout.addWidget(QLabel("Max delay (s)"))
        random_interval_layout.addWidget(self.max_delay_input)

        self.interval_stacked_layout.addWidget(self.fixed_interval_widget)
        self.interval_stacked_layout.addWidget(self.random_interval_widget)
        interval_layout.addLayout(self.interval_stacked_layout)

        main_layout.addWidget(self.interval_group)

        # Group Box for Combo Keys
        combo_keys_group = QGroupBox("Combo Keys")
        combo_keys_layout = QHBoxLayout()
        combo_keys_group.setLayout(combo_keys_layout)

        self.ctrl_checkbox = QCheckBox("Ctrl")
        self.alt_checkbox = QCheckBox("Alt")
        self.shift_checkbox = QCheckBox("Shift")
        combo_keys_layout.addWidget(self.ctrl_checkbox)
        combo_keys_layout.addWidget(self.alt_checkbox)
        combo_keys_layout.addWidget(self.shift_checkbox)

        main_layout.addWidget(combo_keys_group)

        # Sound Effect Option
        self.sound_effect_checkbox = QCheckBox("Sound effect on key press")
        main_layout.addWidget(self.sound_effect_checkbox)

        # Start and Stop Buttons
        self.start_stop_layout = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.start_button.setObjectName("startButton")
        self.start_button.clicked.connect(self.start_presser)
        self.start_stop_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setObjectName("stopButton")
        self.stop_button.clicked.connect(self.stop_presser)
        self.start_stop_layout.addWidget(self.stop_button)

        main_layout.addLayout(self.start_stop_layout)

        self.setLayout(main_layout)
        self.update_random_delay_visibility()

        # Apply CSS Styles
        self.applyStyles()
        self.adjustSize()

    def applyStyles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f9f9f9;
                font-family: Arial, sans-serif;
            }
            QGroupBox {
                border: 1px solid #d3d3d3;
                border-radius: 5px;
                margin-top: 10px;
                padding: 10px;
                font-weight: bold;
                color: #333;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px;
                background-color: #e6e6e6;
                border-radius: 5px;
            }
            QLabel {
                font-size: 14px;
                color: #555;
            }
            QLabel#title {
                font-size: 16px;
                color: #000000;
                font-weight: bold;
                margin-bottom: 10px;
                border: 1px solid #d3d3d3;
                border-radius: 5px;
                padding: 5px;
            }
            QComboBox, QSpinBox, QLineEdit {
                padding: 5px;
                margin: 5px 0;
                border: 1px solid #d3d3d3;
                border-radius: 5px;
            }
            QPushButton {
                font-size: 16px;
                color: #fff;
                background-color: #0078d7;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                margin: 10px 0;
            }
            QPushButton:hover {
                background-color: #005bb5;
            }
            QPushButton:pressed {
                background-color: #003f8a;
            }
            QPushButton:focus {
                outline: none;
            }
            QPushButton#startButton {
                background-color: #28a745;
                max-width: 100%;
            }
            QPushButton#startButton:hover {
                background-color: #218838;
                max-width: 100%;
            }
            QPushButton#startButton:pressed {
                background-color: #1e7e34;
                max-width: 100%;
            }
            QPushButton#stopButton {
                background-color: #dc3545;
                max-width: 100%;
            }
            QPushButton#stopButton:hover {
                background-color: #c82333;
                max-width: 100%;
            }
            QPushButton#stopButton:pressed {
                background-color: #bd2130;'
                max-width: 100%;
            }
        """)

    def initShortcuts(self):
        self.start_shortcut = QShortcut(QKeySequence(self.start_hotkey), self)
        self.start_shortcut.activated.connect(self.start_presser)

        self.stop_shortcut = QShortcut(QKeySequence(self.stop_hotkey), self)
        self.stop_shortcut.activated.connect(self.stop_presser)

    def update_random_delay_visibility(self):
        if self.random_delay_checkbox.isChecked():
            self.interval_stacked_layout.setCurrentWidget(self.random_interval_widget)
        else:
            self.interval_stacked_layout.setCurrentWidget(self.fixed_interval_widget)

    def get_interval(self):
        hours = self.hours_input.value()
        minutes = self.minutes_input.value()
        seconds = self.seconds_input.value()
        milliseconds = self.milliseconds_input.value()
        total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000.0
        return total_seconds

    def start_presser(self):
        time.sleep(2)
        if not self.is_running:
            self.is_running = True
            interval = self.get_interval()
            key = self.key_input.text()
            random_delay = self.random_delay_checkbox.isChecked()
            min_delay = self.min_delay_input.value()
            max_delay = self.max_delay_input.value()
            press_times_mode = "X times" if self.repeat_radio.isChecked() else "Infinite (Until Stopped)"
            press_times = self.press_times_input.value() if press_times_mode == "X times" else -1
            hold_key = self.hold_key_checkbox.isChecked()
            continuous_hold = self.continuous_hold_checkbox.isChecked()
            modifiers = {
                'ctrl': self.ctrl_checkbox.isChecked(),
                'alt': self.alt_checkbox.isChecked(),
                'shift': self.shift_checkbox.isChecked()
            }
            sound_effect = self.sound_effect_checkbox.isChecked()
            self.thread = threading.Thread(target=self.press_key, args=(key, interval, random_delay, min_delay, max_delay, press_times, hold_key, continuous_hold, modifiers, sound_effect))
            self.thread.start()

    def stop_presser(self):
        if self.is_running:
            self.is_running = False
            if self.thread is not None:
                self.thread.join()

    def press_key(self, key, interval, random_delay, min_delay, max_delay, press_times, hold_key, continuous_hold, modifiers, sound_effect):
        presses = 0

        def play_sound():
            if sound_effect:
                print("Beep")

        def press_with_modifiers(k):
            if modifiers['ctrl']:
                print('Ctrl down')
            if modifiers['alt']:
                print('Alt down')
            if modifiers['shift']:
                print('Shift down')

            print(f'Press {k}')

            if modifiers['ctrl']:
                print('Ctrl up')
            if modifiers['alt']:
                print('Alt up')
            if modifiers['shift']:
                print('Shift up')

            play_sound()

        if continuous_hold:
            print(f'Key {key} down')
            play_sound()
            while self.is_running:
                pass  # Keep the key pressed continuously
            print(f'Key {key} up')
            return

        while self.is_running and (press_times == -1 or presses < press_times):
            if random_delay:
                interval = random.uniform(min_delay, max_delay)

            if hold_key:
                if modifiers['ctrl'] or modifiers['alt'] or modifiers['shift']:
                    press_with_modifiers(key)
                else:
                    print(f'Key {key} down')
                    print(f'Wait {interval}')
                    print(f'Key {key} up')
                    play_sound()
            else:
                if modifiers['ctrl'] or modifiers['alt'] or modifiers['shift']:
                    press_with_modifiers(key)
                else:
                    print(f'Press {key}')
                    play_sound()
                    print(f'Wait {interval}')

            presses += 1

    def get_settings(self):
        return {
            'key': self.key_input.text(),
            'interval': self.get_interval(),
            'random_delay': self.random_delay_checkbox.isChecked(),
            'min_delay': self.min_delay_input.value(),
            'max_delay': self.max_delay_input.value(),
            'click_times_mode': self.click_times_combo.currentText(),
            'click_times': self.click_times_input.value(),
            'hold_key': self.hold_key_checkbox.isChecked(),
            'continuous_hold': self.continuous_hold_checkbox.isChecked(),
            'modifiers': {
                'ctrl': self.ctrl_checkbox.isChecked(),
                'alt': self.alt_checkbox.isChecked(),
                'shift': self.shift_checkbox.isChecked()
            },
            'sound_effect': self.sound_effect_checkbox.isChecked(),
        }

    def updateSettings(self, settings):
        self.key_input.setText(settings['key'])
        interval = settings['interval']
        self.hours_input.setValue(interval // 3600)
        self.minutes_input.setValue((interval % 3600) // 60)
        self.seconds_input.setValue(interval % 60)
        self.milliseconds_input.setValue(int((interval * 1000) % 1000))
        self.random_delay_checkbox.setChecked(settings['random_delay'])
        self.min_delay_input.setValue(settings['min_delay'])
        self.max_delay_input.setValue(settings['max_delay'])
        self.click_times_combo.setCurrentText(settings['click_times_mode'])
        self.click_times_input.setValue(settings['click_times'])
        self.hold_key_checkbox.setChecked(settings['hold_key'])
        self.continuous_hold_checkbox.setChecked(settings['continuous_hold'])
        self.ctrl_checkbox.setChecked(settings['modifiers']['ctrl'])
        self.alt_checkbox.setChecked(settings['modifiers']['alt'])
        self.shift_checkbox.setChecked(settings['modifiers']['shift'])
        self.sound_effect_checkbox.setChecked(settings['sound_effect'])

    def get_default_settings(self):
        return {
            'key': '',
            'interval': 1.0,
            'random_delay': False,
            'min_delay': 0,
            'max_delay': 0,
            'click_times_mode': 'Infinite (Until Stopped)',
            'click_times': 1,
            'hold_key': False,
            'continuous_hold': False,
            'modifiers': {
                'ctrl': False,
                'alt': False,
                'shift': False
            },
            'sound_effect': False,
        }

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = KeyPresser()
    ex.show()
    sys.exit(app.exec_())
