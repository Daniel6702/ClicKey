from PyQt5.QtWidgets import QWidget, QCheckBox
from PyQt5.QtCore import pyqtSignal, Qt

from base_components.gui_components.title_widget import TitleWidget
from base_components.gui_components.start_stop_widget import StartStopWidget
from base_components.gui_components.interval_widget import IntervalWidget
from base_components.gui_components.repetition_widget import RepeatActionWidget

class BaseAutoActionGUI(QWidget):
    changeSettings = pyqtSignal(dict, name='changeSettings')

    def __init__(self, title: str):
        super().__init__()

        self.title_widget = TitleWidget(title)
        self.start_stop_widget = StartStopWidget()
        self.start_stop_widget.change_status.connect(self.title_widget.change_status.emit)

        self.sound_effect_checkbox = QCheckBox("Sound effect")
        self.sound_effect_checkbox.stateChanged.connect(lambda: self.changeSettings.emit({'sound_effect': self.sound_effect_checkbox.isChecked()}))

        self.interval_widget = IntervalWidget()
        self.interval_widget.change_settings.connect(self.changeSettings.emit)

        self.repeat_action_widget = RepeatActionWidget()
        self.repeat_action_widget.change_settings.connect(self.changeSettings.emit)

    def stop(self):
        self.start_stop_widget.change_status.emit(False)
        self.title_widget.change_status.emit(False)

    def update_settings(self, new_settings: dict):
        if new_settings.get('sound_effect', None):
            self.sound_effect_checkbox.setChecked(new_settings['sound_effect'])
        if new_settings.get('repeat_inf', None):
            self.repeat_action_widget.repeat_radio.setChecked(not new_settings['repeat_inf'])
            self.repeat_action_widget.repeat_until_stopped_radio.setChecked(new_settings['repeat_inf'])
        if new_settings.get('repeat_times', None):
            self.repeat_action_widget.press_times_input.setValue(new_settings['repeat_times'])
        if new_settings.get('interval_norm', None):
            total_seconds = new_settings['interval_norm']
            hours = total_seconds // 3600  
            remainder = total_seconds % 3600 
            minutes = remainder // 60  
            seconds = remainder % 60  
            milliseconds = (total_seconds - int(total_seconds)) * 1000 
            self.interval_widget.hours_input.setValue(int(hours))
            self.interval_widget.minutes_input.setValue(int(minutes))
            self.interval_widget.seconds_input.setValue(int(seconds))
            self.interval_widget.milliseconds_input.setValue(int(milliseconds))
        if new_settings.get('random_interval', None): 
            self.interval_widget.interval_stacked_layout.setCurrentIndex(new_settings['random_interval'])
            self.interval_widget.random_delay_checkbox.setChecked(new_settings['random_interval'])
        if new_settings.get('min_delay', None):
            self.interval_widget.min_delay_input.setValue(new_settings['min_delay'])
        if new_settings.get('max_delay', None):
            self.interval_widget.max_delay_input.setValue(new_settings['max_delay'])
