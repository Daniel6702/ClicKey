from base_components.base_logic import BaseLogic
from PyQt5.QtCore import pyqtSignal
import json
import os
from PyQt5.QtWidgets import QFileDialog

PROFILES_PATH = 'modules/profile_manager/profiles'

class ProfilesLogic(BaseLogic):
    add_profile = pyqtSignal(dict, name='addProfile')

    def __init__(self):
        super().__init__()
        self.controllers = []
        self.settings_files = []

    def get_settings(self) -> dict:
        settings = {}
        for controller in self.controllers:
            controller_type = controller.logic.__class__.__name__
            settings[controller_type] = controller.get_settings()
        return settings
        
    def get_default_settings(self) -> dict:
        return {"name": "Default Profile", "settings": self.get_settings()}
    
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
        try:
            os.remove(f"{PROFILES_PATH}/{name}.json")
        except FileNotFoundError:
            print("File not found")

    def apply_profile(self, profile: dict):
        '''
        For each controller in system, retrieve Type (Name of logic class) corresponding to the key in the profile settings.
        Retrieve settings for that controller from profile dict with the key (type).
        Update settings for that controller.
        '''
        for controller in self.controllers:
            controller_type = controller.logic.__class__.__name__
            profile_settings = profile.get("settings", {})
            controller.update_settings(profile_settings.get(controller_type, {}))
        print(f"Applied profile: {profile}")
    
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