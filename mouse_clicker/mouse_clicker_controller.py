from base_components.controller import AutoActionController
from mouse_clicker.clicker_logic import ClickerLogic
from mouse_clicker.clicker_gui import ClickerGUI
from PyQt5.QtWidgets import QWidget

class ClickerController(AutoActionController, QWidget):
    def __init__(self):
        super().__init__(ClickerLogic, ClickerGUI, "settings/mouse_clicker_settings.json")
