from base_components.controller import AutoActionController
from PyQt5.QtWidgets import QWidget
from key_presser.presser_logic import KeyPresserLogic
from key_presser.presser_gui import KeyPresserGUI

class PresserController(AutoActionController, QWidget):
    def __init__(self):
        super().__init__(KeyPresserLogic, KeyPresserGUI, 'settings/key_presser_settings.json')
        