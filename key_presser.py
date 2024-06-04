import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QSpinBox, QCheckBox, QPushButton, QHBoxLayout, QComboBox, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut
import random
import threading

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
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        self.key_input = QLineEdit(self)
        layout.addWidget(QLabel("Key:"))
        layout.addWidget(self.key_input)
        
        layout.addWidget(QLabel("Interval between presses:"))
        interval_layout = QHBoxLayout()
        self.hours_input = QSpinBox(self)
        self.hours_input.setRange(0, 23)
        self.minutes_input = QSpinBox(self)
        self.minutes_input.setRange(0, 59)
        self.seconds_input = QSpinBox(self)
        self.seconds_input.setRange(0, 59)
        self.milliseconds_input = QSpinBox(self)
        self.milliseconds_input.setRange(0, 999)
        interval_layout.addWidget(QLabel("Hours"))
        interval_layout.addWidget(self.hours_input)
        interval_layout.addWidget(QLabel("Minutes"))
        interval_layout.addWidget(self.minutes_input)
        interval_layout.addWidget(QLabel("Seconds"))
        interval_layout.addWidget(self.seconds_input)
        interval_layout.addWidget(QLabel("Milliseconds"))
        interval_layout.addWidget(self.milliseconds_input)
        layout.addLayout(interval_layout)

        self.random_delay_checkbox = QCheckBox("Random delay within range")
        self.random_delay_checkbox.stateChanged.connect(self.update_random_delay_visibility)
        layout.addWidget(self.random_delay_checkbox)

        self.random_delay_layout = QHBoxLayout()
        self.min_delay_input = QSpinBox(self)
        self.min_delay_input.setRange(0, 3600)
        self.max_delay_input = QSpinBox(self)
        self.max_delay_input.setRange(0, 3600)
        self.random_delay_layout.addWidget(QLabel("Min delay (s)"))
        self.random_delay_layout.addWidget(self.min_delay_input)
        self.random_delay_layout.addWidget(QLabel("Max delay (s)"))
        self.random_delay_layout.addWidget(self.max_delay_input)
        layout.addLayout(self.random_delay_layout)

        self.click_times_combo = QComboBox(self)
        self.click_times_combo.addItems(["Infinite (Until Stopped)", "X times"])
        self.click_times_combo.currentIndexChanged.connect(self.update_click_times_visibility)
        layout.addWidget(QLabel("Number of Presses:"))
        layout.addWidget(self.click_times_combo)

        self.click_times_input = QSpinBox(self)
        self.click_times_input.setMinimum(1)
        self.click_times_input.setMaximum(1000000)
        self.click_times_input.setValue(1)
        layout.addWidget(self.click_times_input)

        self.hold_key_checkbox = QCheckBox("Hold key pressed between presses")
        layout.addWidget(self.hold_key_checkbox)

        self.continuous_hold_checkbox = QCheckBox("Continuously hold key pressed")
        layout.addWidget(self.continuous_hold_checkbox)
        
        layout.addWidget(QLabel("Combo Key (Optional):"))
        self.ctrl_checkbox = QCheckBox("Ctrl")
        self.alt_checkbox = QCheckBox("Alt")
        self.shift_checkbox = QCheckBox("Shift")
        combo_layout = QHBoxLayout()
        combo_layout.addWidget(self.ctrl_checkbox)
        combo_layout.addWidget(self.alt_checkbox)
        combo_layout.addWidget(self.shift_checkbox)
        layout.addLayout(combo_layout)

        self.sound_effect_checkbox = QCheckBox("Sound effect on key press")
        layout.addWidget(self.sound_effect_checkbox)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_presser)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_presser)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)
        self.update_random_delay_visibility()
        self.update_click_times_visibility()

    def initShortcuts(self):
        self.start_shortcut = QShortcut(QKeySequence(self.start_hotkey), self)
        self.start_shortcut.activated.connect(self.start_presser)

        self.stop_shortcut = QShortcut(QKeySequence(self.stop_hotkey), self)
        self.stop_shortcut.activated.connect(self.stop_presser)

    def update_random_delay_visibility(self):
        is_random_delay = self.random_delay_checkbox.isChecked()
        for i in range(self.random_delay_layout.count()):
            self.random_delay_layout.itemAt(i).widget().setVisible(is_random_delay)

    def update_click_times_visibility(self):
        mode = self.click_times_combo.currentText()
        is_x_times = mode == "X times"
        self.click_times_input.setVisible(is_x_times)

    def get_interval(self):
        hours = self.hours_input.value()
        minutes = self.minutes_input.value()
        seconds = self.seconds_input.value()
        milliseconds = self.milliseconds_input.value()
        total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000.0
        return total_seconds

    def start_presser(self):
        if not self.is_running:
            self.is_running = True
            interval = self.get_interval()
            key = self.key_input.text()
            random_delay = self.random_delay_checkbox.isChecked()
            min_delay = self.min_delay_input.value()
            max_delay = self.max_delay_input.value()
            click_times_mode = self.click_times_combo.currentText()
            click_times = self.click_times_input.value() if click_times_mode == "X times" else -1
            hold_key = self.hold_key_checkbox.isChecked()
            continuous_hold = self.continuous_hold_checkbox.isChecked()
            modifiers = {
                'ctrl': self.ctrl_checkbox.isChecked(),
                'alt': self.alt_checkbox.isChecked(),
                'shift': self.shift_checkbox.isChecked()
            }
            sound_effect = self.sound_effect_checkbox.isChecked()
            # Removed macro_steps from arguments
            self.thread = threading.Thread(target=self.press_key, args=(key, interval, random_delay, min_delay, max_delay, click_times, hold_key, continuous_hold, modifiers, sound_effect))
            self.thread.start()

    def stop_presser(self):
        if self.is_running:
            self.is_running = False
            if self.thread is not None:
                self.thread.join()

    def press_key(self, key, interval, random_delay, min_delay, max_delay, click_times, hold_key, continuous_hold, modifiers, sound_effect):
        presses = 0

        def play_sound():
            if sound_effect:
                # Replaced winsound with a placeholder function as it is Windows specific
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

        while self.is_running and (click_times == -1 or presses < click_times):
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
