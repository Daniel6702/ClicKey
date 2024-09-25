from modules.settings.settings_logic import SettingsLogic
from modules.settings.settings_gui import SettingsGUI
from base_components.base_controller import BaseController
from PyQt5.QtWidgets import QWidget

class SettingsController(BaseController, QWidget):
    def __init__(self):
        super().__init__(SettingsLogic, SettingsGUI, 'default_settings/key_presser_settings.json')
        self.gui.theme_changed.connect(self.logic.theme_changed)
        self.gui.delay_changed.connect(self.logic.delay_changed)
        self.gui.hide_in_tray.connect(self.logic.hide_in_system_tray)