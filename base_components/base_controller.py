from base_components.base_logic import BaseLogic
from base_components.base_gui import BaseGUI

class BaseController():
    def __init__(self, logic_class: type[BaseLogic], gui_class: type[BaseGUI], default_settings_file: str):
        self.logic = logic_class()
        self.gui = gui_class()
        
        self.logic.load_json_settings(default_settings_file)
        self.gui.changeSettings.connect(self.logic.update_settings)
        self.gui.start_stop_widget.change_status.connect(self.logic.change_status)
        self.logic.stop_signal.connect(self.gui.stop)

    def get_settings(self):
        return self.logic.settings
    
    def update_settings(self, new_settings: dict):
        self.logic.settings = new_settings
        self.gui.update_settings(new_settings)