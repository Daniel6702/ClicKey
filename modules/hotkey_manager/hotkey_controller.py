from modules.hotkey_manager.hotkey_logic import HotkeyLogic
from modules.hotkey_manager.hotkey_gui import HotkeyGUI
from base_components.base_controller import BaseController
from PyQt5.QtWidgets import QWidget

class HotkeyController(BaseController, QWidget):
    def __init__(self):
        super().__init__(HotkeyLogic, HotkeyGUI, 'default_settings/key_presser_settings.json')
        self.gui.hot_key_changed.connect(self.logic.update_hotkey)
        self.gui.initClickerUI()

    def add_controllers(self, controllers: list[type[BaseController]]) -> None:
        self.logic.controllers = controllers