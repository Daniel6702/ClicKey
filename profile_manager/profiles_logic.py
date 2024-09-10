from base_components.base_logic import BaseAutoActionLogic
from PyQt5.QtCore import pyqtSignal
import json
import os
from PyQt5.QtWidgets import QFileDialog

PROFILES_PATH = 'profile_manager/profiles'

class ProfilesLogic(BaseAutoActionLogic):
    add_profile = pyqtSignal(dict, name='addProfile')

    def __init__(self):
        super().__init__()
        self.controllers = []
        self.settings_files = []

    def get_settings(self) -> list[dict]:
        return [controller.logic.settings for controller in self.controllers]
        
    def get_default_settings(self) -> dict:
        settings = []
        for file in self.settings_files:
            settings.append(self.load_json_settings(file))
        return {"name": "Default Profile", "settings": settings}
    
    def compare_dict_keys(self, dict1: dict, dict2: dict) -> bool:
        return set(dict1.keys()) == set(dict2.keys())
    
    def update_settings(self, new_settings: dict):
        for controller in self.controllers:
            if self.compare_dict_keys(controller.settings, new_settings):
                controller.update_settings(new_settings)
                return True
        return False
    
    def load_profiles(self, path: str = PROFILES_PATH):
        profiles = []
        for file in os.listdir(path):
            if file.endswith('.json'):
                with open(f"{path}/{file}", 'r') as f:
                    file_name = os.path.splitext(file)[0]
                    profiles.append(json.load(f))
        for profile in profiles:
            self.add_profile.emit(profile)
    
    def save_json_settings(self, settings, file_path: str = 'settings.json'):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            json.dump(settings, file, indent=4)

    def delete_profile(self, name: str):
        print(f"Deleting profile file: {name}.json")
        os.remove(f"{PROFILES_PATH}/{name}.json")

    def conver_str_to_dict(self, string: str) -> dict:
        return json.loads(string)

    def apply_profile(self, profile: dict):
        '''
        for each controller get its current settings
        loop through list in profile dict
        find the one that matches all the keys
        update the controller settings with the profile settings
        '''
        print(f"Applying profile: {profile}, TYPE: {type(profile)}")
        for controller in self.controllers:
            controller_settings = controller.get_settings()
            for profile_settings in profile.get('settings', []):
                print(profile_settings)
                if isinstance(profile_settings, str):
                    profile_settings = self.conver_str_to_dict(profile_settings)
                    
                if self.compare_dict_keys(controller_settings, profile_settings):
                    controller.update_settings(profile_settings)
                    break
        print(f"Applying profile: {profile}")
    
    def save_profile(self, name: str):
        profile = {"name": name, "settings": self.get_settings()}
        self.add_profile.emit(profile)
        self.save_json_settings(profile, f"{PROFILES_PATH}/{name}.json")

    def load_profile_from_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(None, "Load Profile", "", "Text Files (*.json);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'r') as file:
                    settings = json.load(file)
                    profile_name = os.path.splitext(os.path.basename(file_name))[0]
                    if settings.get('name', None):
                        settings = settings.get('settings', [])
                self.add_profile.emit({"name": profile_name, "settings": settings})
            except FileNotFoundError:
                print("File not Found")