from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QTextEdit, QCheckBox, QHBoxLayout, QListWidget, QLabel, QWidget, QInputDialog
from base_components.base_gui import BaseGUI
from PyQt5.QtCore import Qt, pyqtSignal

class ProfilesGUI(BaseGUI):
    save_profile_signal = pyqtSignal(str)
    delete_profile_signal = pyqtSignal(str)
    load_profile_signal = pyqtSignal()
    apply_profile_signal = pyqtSignal(dict)

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

        self.save_button = QPushButton("Save Profile", self)
        self.save_button.clicked.connect(self.open_name_input_dialog)
        button_layout.addWidget(self.save_button)

        self.apply_button = QPushButton("Apply Profile")
        self.apply_button.clicked.connect(self.apply)
        button_layout.addWidget(self.apply_button)

        self.load_button = QPushButton("Load Profile")
        self.load_button.clicked.connect(lambda: self.load_profile_signal.emit())
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
        selected_profile = self.profile_list.currentItem().text()
        for profile in self.profiles:
            if profile.get('name') == selected_profile:
                self.apply_profile_signal.emit(profile)
                print(f"Applying profile: {selected_profile}")
                break

    def save_profile(self):
        pass

    def delete_profile(self):
        selected_profile = self.profile_list.currentItem().text()
        self.delete_profile_signal.emit(selected_profile)
        self.profile_list.takeItem(self.profile_list.currentRow())
        print(f"Deleting profile: {selected_profile}")

    def profile_selected(self, item):
        profile_name = item.text()
        print(f"Profile selected: {profile_name}")

    def add_profile(self, profile: dict):
        self.profiles.append(profile)
        self.profile_list.addItem(profile.get('name', ''))
        print(f"Profile added: {profile.get('name', '')}")
        

    def open_name_input_dialog(self):
        name, ok = QInputDialog.getText(self, 'Enter Name', 'Please enter your name:')
        
        if ok and name:
            self.save_profile_signal.emit(name)
