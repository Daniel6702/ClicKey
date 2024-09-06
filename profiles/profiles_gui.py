from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QTextEdit, QCheckBox, QHBoxLayout, QListWidget, QLabel, QWidget
from base_components.base_gui import BaseAutoActionGUI
from PyQt5.QtCore import Qt, pyqtSignal

class ProfilesGUI(BaseAutoActionGUI):
    def __init__(self):
        super().__init__("Profiles")
        self.profiles = []
        self.initProfilesUI()

    def initProfilesUI(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        # Title widget
        self.title_widget.status_label.setText("")
        main_layout.addWidget(self.title_widget)

        temp_H = QHBoxLayout()

        # Profile buttons
        button_layout = QVBoxLayout()

        self.save_button = QPushButton("Save Profile")
        self.save_button.clicked.connect(self.save_profile)
        button_layout.addWidget(self.save_button)

        self.apply_button = QPushButton("Apply Profile")
        self.apply_button.clicked.connect(self.apply)
        button_layout.addWidget(self.apply_button)

        self.load_button = QPushButton("Load Profile")
        self.load_button.clicked.connect(self.load_profile)
        button_layout.addWidget(self.load_button)

        self.delete_button = QPushButton("Delete Profile")
        self.delete_button.clicked.connect(self.delete_profile)
        button_layout.addWidget(self.delete_button)

        temp_H.addLayout(button_layout)

        # Profile List Widget
        self.profile_list = QListWidget(self)
        self.profile_list.itemClicked.connect(self.profile_selected) 
        temp_H.addWidget(self.profile_list)

        main_layout.addLayout(temp_H)

        self.setLayout(main_layout)

    def apply(self):
        pass

    def save_profile(self):
        pass

    def load_profile(self):
        selected_profile = self.profile_list.currentItem().text()
        print(f"Loading profile: {selected_profile}")

    def delete_profile(self):
        selected_profile = self.profile_list.currentItem().text()
        print(f"Deleting profile: {selected_profile}")

    def profile_selected(self, item):
        profile_name = item.text()
        print(f"Profile selected: {profile_name}")

    def update_gui(self, add_profile: bool = False, profile: dict = {}):
        if add_profile:
            self.profiles.append(profile)
            self.profile_list.addItem(profile.get('name', ''))
            print(f"Profile added: {profile.get('name', '')}")