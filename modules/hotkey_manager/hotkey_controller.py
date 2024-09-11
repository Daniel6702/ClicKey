from modules.hotkey_manager.hotkey_logic import HotkeyLogic
from modules.hotkey_manager.hotkey_gui import HotkeyGUI
from base_components.controller import AutoActionController
from PyQt5.QtWidgets import QWidget

class HotkeyController(AutoActionController, QWidget):
    def __init__(self):
        super().__init__(HotkeyLogic, HotkeyGUI, 'default_settings/key_presser_settings.json')
        self.gui.hot_key_changed.connect(self.logic.update_hotkey)
        self.gui.initClickerUI()

    def add_controllers(self, controllers: list[type[AutoActionController]]) -> None:
        self.logic.controllers = controllers