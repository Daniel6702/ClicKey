from base_components.controller import AutoActionController
from profiles.profiles_logic import ProfilesLogic
from profiles.profiles_gui import ProfilesGUI

class ProfilesController(AutoActionController):
    def __init__(self, controllers: list[type[AutoActionController]], settings_files: list[str]):
        self.gui = ProfilesGUI()
        self.logic = ProfilesLogic(controllers, self.update_GUI, settings_files)
        self.gui.changeSettings.connect(self.logic.update_settings)
        self.gui.changeStatus.connect(self.logic.change_status)
        self.gui.show()