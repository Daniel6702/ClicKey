from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QFileDialog, QApplication, QGroupBox
from PyQt5.QtCore import pyqtSignal
import json
import os
import sys

class Profiles(QWidget):
    profileLoaded = pyqtSignal(dict)

    def __init__(self, profile_manager, main_app):
        super().__init__()
        self.profile_manager = profile_manager
        self.main_app = main_app  # Store the reference to MainApp
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        self.title = QLabel("Profiles Section")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title) 

        # Profile Actions
        profile_actions_group = QGroupBox("")
        profile_actions_layout = QVBoxLayout()
        profile_actions_group.setLayout(profile_actions_layout)

        self.save_button = QPushButton("Save Profile")
        self.save_button.clicked.connect(self.save_profile)
        profile_actions_layout.addWidget(self.save_button)

        self.load_button = QPushButton("Load Profile")
        self.load_button.clicked.connect(self.load_profile)
        profile_actions_layout.addWidget(self.load_button)

        self.reset_button = QPushButton("Reset to Default Profile")
        self.reset_button.clicked.connect(self.reset_to_default)
        profile_actions_layout.addWidget(self.reset_button)

        main_layout.addWidget(profile_actions_group)

        self.setLayout(main_layout)

        # Apply CSS Styles
        self.applyStyles()

    def applyStyles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f9f9f9;
                font-family: Arial, sans-serif;
            }
            QGroupBox {
                border: 1px solid #d3d3d3;
                border-radius: 5px;
                margin-top: 10px;
                padding: 10px;
                font-weight: bold;
                color: #333;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px;
                background-color: #e6e6e6;
                border-radius: 5px;
            }
            QLabel {
                font-size: 14px;
                color: #555;
            }
            QLabel#title {
                font-size: 16px;
                color: #000000;
                font-weight: bold;
                margin-bottom: 10px;
                border: 1px solid #d3d3d3;
                border-radius: 5px;
                padding: 5px;
            }
            QComboBox, QSpinBox, QLineEdit, QTextEdit {
                padding: 5px;
                margin: 5px 0;
                border: 1px solid #d3d3d3;
                border-radius: 5px;
            }
            QPushButton {
                font-size: 16px;
                color: #fff;
                background-color: #0078d7;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                margin: 10px 0;
            }
            QPushButton:hover {
                background-color: #005bb5;
            }
            QPushButton:pressed {
                background-color: #003f8a;
            }
            QPushButton:focus {
                outline: none;
            }
            QPushButton#startButton {
                background-color: #28a745;
                max-width: 100%;
            }
            QPushButton#startButton:hover {
                background-color: #218838;
                max-width: 100%;
            }
            QPushButton#startButton:pressed {
                background-color: #1e7e34;
                max-width: 100%;
            }
            QPushButton#stopButton {
                background-color: #dc3545;
                max-width: 100%;
            }
            QPushButton#stopButton:hover {
                background-color: #c82333;
                max-width: 100%;
            }
            QPushButton#stopButton:pressed {
                background-color: #bd2130;'
                max-width: 100%;
            }
        """)

    def save_profile(self):
        profile_name, _ = QFileDialog.getSaveFileName(self, "Save Profile", "", "JSON Files (*.json);;All Files (*)")
        if profile_name:
            settings = {
                'mouse_clicker': self.main_app.mouse_clicker.get_settings(),  # Use main_app reference
                'key_presser': self.main_app.key_presser.get_settings(),
                'scripts': self.main_app.scripts.get_settings(),
                'settings': self.main_app.settings.get_settings(),
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
            'mouse_clicker': self.main_app.mouse_clicker.get_default_settings(),  # Use main_app reference
            'key_presser': self.main_app.key_presser.get_default_settings(),
            'scripts': self.main_app.scripts.get_default_settings(),
            'settings': self.main_app.settings.get_default_settings(),
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