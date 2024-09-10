from base_components.controller import AutoActionController
from PyQt5.QtWidgets import QWidget
from modules.key_presser.presser_logic import KeyPresserLogic
from modules.key_presser.presser_gui import KeyPresserGUI

class PresserController(AutoActionController, QWidget):
    def __init__(self):
        super().__init__(KeyPresserLogic, KeyPresserGUI, 'default_settings/key_presser_settings.json')
        