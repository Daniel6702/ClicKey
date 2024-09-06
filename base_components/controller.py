from base_components.base_logic import BaseAutoActionLogic
from base_components.base_gui import BaseAutoActionGUI

class AutoActionController():
    def __init__(self, logic_class: type[BaseAutoActionLogic], gui_class: type[BaseAutoActionGUI], settings_file: str = None, show: bool = True):
        self.logic = logic_class(self.update_GUI, settings_file)
        self.gui = gui_class()

        self.gui.changeSettings.connect(self.logic.update_settings)
        self.gui.changeStatus.connect(self.logic.change_status)

        self.logic.load_json_settings(settings_file)
        if show: self.gui.show()

    def update_GUI(self, *args, **kwargs):
        self.gui.update_gui(*args, **kwargs)