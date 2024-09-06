from base_components.base_logic import BaseAutoActionLogic
from base_components.controller import AutoActionController

class ProfilesLogic(BaseAutoActionLogic):
    def __init__(self, controllers: list[type[BaseAutoActionLogic]], update_GUI, settings_files: list[str] = None):
        super().__init__(update_GUI)
        self.controllers = controllers
        self.settings_files = settings_files
        self.default_settings = self.get_default_settings()
        self.update_GUI(add_profile=True, profile = {"name": "Default", "settings": self.default_settings})

    def get_settings(self) -> list[dict]:
        return [controller.settings for controller in self.controllers]
        
    def get_default_settings(self) -> dict:
        settings = []
        for file in self.settings_files:
            settings.append(self.load_json_settings(file))
        return settings
    
    def compare_dict_keys(dict1: dict, dict2: dict) -> bool:
        return set(dict1.keys()) == set(dict2.keys())
    
    def update_settings(self, new_settings: dict):
        for controller in self.controllers:
            if self.compare_dict_keys(controller.settings, new_settings):
                controller.update_settings(new_settings)
                return True
        return False