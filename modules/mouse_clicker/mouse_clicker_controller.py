from base_components.base_controller import BaseController
from modules.mouse_clicker.clicker_logic import ClickerLogic
from modules.mouse_clicker.clicker_gui import ClickerGUI
from PyQt5.QtWidgets import QWidget

class ClickerController(BaseController, QWidget):
    def __init__(self):
        super().__init__(ClickerLogic, ClickerGUI, 'default_settings/key_presser_settings.json')
        #AutoActionController.__init__(self, ClickerLogic, ClickerGUI, "default_settings/mouse_clicker_settings.json")
        #QWidget.__init__(self)