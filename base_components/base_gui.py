from PyQt5.QtWidgets import QWidget, QCheckBox
from PyQt5.QtCore import pyqtSignal

from base_components.gui_components.title_widget import TitleWidget
from base_components.gui_components.start_stop_widget import StartStopWidget
from base_components.gui_components.interval_widget import IntervalWidget
from base_components.gui_components.repetition_widget import RepeatActionWidget

class BaseAutoActionGUI(QWidget):
    changeSettings = pyqtSignal(dict, name='changeSettings')
    changeStatus = pyqtSignal(bool)

    def __init__(self, title: str):
        super().__init__()

        self.title_widget = TitleWidget(title)

        self.start_stop_widget = StartStopWidget()
        self.start_stop_widget.change_status.connect(self.changeStatus.emit)
        self.start_stop_widget.change_status.connect(self.title_widget.change_status.emit)

        self.sound_effect_checkbox = QCheckBox("Sound effect")
        self.sound_effect_checkbox.stateChanged.connect(lambda: self.changeSettings.emit({'sound_effect': self.sound_effect_checkbox.isChecked()}))

        self.interval_widget = IntervalWidget()
        self.interval_widget.change_settings.connect(self.changeSettings.emit)

        self.repeat_action_widget = RepeatActionWidget()
        self.repeat_action_widget.change_settings.connect(self.changeSettings.emit)

    def update_gui(self):
        self.start_stop_widget.change_status.emit(False)
        self.title_widget.change_status.emit(False)




