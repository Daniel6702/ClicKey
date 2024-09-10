from base_components.controller import AutoActionController
from modules.profile_manager.profiles_logic import ProfilesLogic
from modules.profile_manager.profiles_gui import ProfilesGUI
from PyQt5.QtWidgets import QWidget

DEFAULT_SETTINGS_FILES = ['default_settings/color_tool_settings.json',
                          'default_settings/key_presser_settings.json',
                          'default_settings/mouse_clicker_settings.json',
                          'default_settings/profiles_settings.json',
                          'default_settings/script_runner_settings.json']

class ProfilesController(AutoActionController, QWidget):
    def __init__(self):
        super().__init__(ProfilesLogic, ProfilesGUI, "default_settings/profiles_settings.json")
        self.logic.settings_files = DEFAULT_SETTINGS_FILES
        self.logic.add_profile.connect(self.gui.add_profile)
        self.logic.add_profile.emit(self.logic.get_default_settings())
        self.gui.save_profile_signal.connect(self.logic.save_profile)
        self.gui.delete_profile_signal.connect(self.logic.delete_profile)
        self.gui.load_profile_signal.connect(self.logic.load_profile_from_file)
        self.gui.apply_profile_signal.connect(self.logic.apply_profile)
        self.logic.load_profiles()

    def add_controllers(self, controllers: list[type[AutoActionController]]) -> None:
        self.logic.controllers = controllers