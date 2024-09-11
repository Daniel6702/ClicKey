from base_components.controller import AutoActionController
from modules.mouse_clicker.clicker_logic import ClickerLogic
from modules.mouse_clicker.clicker_gui import ClickerGUI
from PyQt5.QtWidgets import QWidget

class ClickerController(AutoActionController, QWidget):
    def __init__(self):
        super().__init__(ClickerLogic, ClickerGUI, 'default_settings/key_presser_settings.json')
        #AutoActionController.__init__(self, ClickerLogic, ClickerGUI, "default_settings/mouse_clicker_settings.json")
        #QWidget.__init__(self)