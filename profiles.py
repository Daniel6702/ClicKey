from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QFileDialog, QApplication
from PyQt5.QtCore import pyqtSignal
import json
import os
import sys

class Profiles(QWidget):
    profileLoaded = pyqtSignal(dict)

    def __init__(self, profile_manager):
        super().__init__()
        self.profile_manager = profile_manager
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        layout.addWidget(QLabel("Profiles Section"))

        save_button = QPushButton("Save Profile", self)
        save_button.clicked.connect(self.save_profile)
        layout.addWidget(save_button)

        load_button = QPushButton("Load Profile", self)
        load_button.clicked.connect(self.load_profile)
        layout.addWidget(load_button)

        reset_button = QPushButton("Reset to Default Profile", self)
        reset_button.clicked.connect(self.reset_to_default)
        layout.addWidget(reset_button)

        self.setLayout(layout)

    def save_profile(self):
        profile_name, _ = QFileDialog.getSaveFileName(self, "Save Profile", "", "JSON Files (*.json);;All Files (*)")
        if profile_name:
            settings = {
                'mouse_clicker': self.parent().mouse_clicker.get_settings(),
                'key_presser': self.parent().key_presser.get_settings(),
                'scripts': self.parent().scripts.get_settings(),
                'settings': self.parent().settings.get_settings(),
            }
            self.profile_manager.save_profile(profile_name, settings)

    def load_profile(self):
        profile_name, _ = QFileDialog.getOpenFileName(self, "Load Profile", "", "JSON Files (*.json);;All Files (*)")
        if profile_name:
            settings = self.profile_manager.load_profile(profile_name)
            if settings:
                self.profileLoaded.emit(settings)

    def reset_to_default(self):
        default_settings = {
            'mouse_clicker': self.parent().mouse_clicker.get_default_settings(),
            'key_presser': self.parent().key_presser.get_default_settings(),
            'scripts': self.parent().scripts.get_default_settings(),
            'settings': self.parent().settings.get_default_settings(),
        }
        self.profileLoaded.emit(default_settings)


class ProfileManager:
    def save_profile(self, profile_path, settings):
        with open(profile_path, 'w') as profile_file:
            json.dump(settings, profile_file)

    def load_profile(self, profile_path):
        with open(profile_path, 'r') as profile_file:
            return json.load(profile_file)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    profile_manager = ProfileManager()
    profiles = Profiles(profile_manager)
    profiles.resize(400, 500)
    profiles.show()
    sys.exit(app.exec_())