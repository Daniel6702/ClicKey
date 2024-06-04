import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget
from PyQt5.QtCore import Qt

from mouse_clicker import MouseClicker
from key_presser import KeyPresser
from profiles import Profiles
from scripts import Scripts
from settings import Settings

#pynput, pyautogui, pyqt5, pyautogui, sip

class MainApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.initConnections()

    def initUI(self):
        main_layout = QHBoxLayout()
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setAlignment(Qt.AlignTop)

        self.stacked_widget = QStackedWidget(self)

        self.mouse_clicker = MouseClicker()
        self.key_presser = KeyPresser()
        self.profiles = Profiles()
        self.scripts = Scripts()
        self.settings = Settings()

        self.stacked_widget.addWidget(self.mouse_clicker)
        self.stacked_widget.addWidget(self.key_presser)
        self.stacked_widget.addWidget(self.profiles)
        self.stacked_widget.addWidget(self.scripts)
        self.stacked_widget.addWidget(self.settings)

        self.buttons = [
            ("Mouse Clicker", self.mouse_clicker),
            ("Key Presser", self.key_presser),
            ("Profiles", self.profiles),
            ("Scripts", self.scripts),
            ("Settings", self.settings)
        ]

        for i, (name, widget) in enumerate(self.buttons):
            button = QPushButton(name, self)
            button.clicked.connect(lambda _, w=widget: self.stacked_widget.setCurrentWidget(w))
            sidebar_layout.addWidget(button)

        main_layout.addLayout(sidebar_layout)
        main_layout.addWidget(self.stacked_widget)

        self.setLayout(main_layout)
        self.setWindowTitle('Auto Key/Mouse Presser')
        self.resize(500, 600)
        self.show()

    def initConnections(self):
        # Connect settings signals to the appropriate slots
        self.settings.settingsChanged.connect(self.handleSettingsChanged)
        self.settings.emergencyStop.connect(self.handleEmergencyStop)
        self.settings.hideApp.connect(self.handleHideApp)

    def handleSettingsChanged(self, settings):
        print(f"Settings changed: {settings}")
        # Update the application components with the new settings
        self.mouse_clicker.updateSettings(settings)
        self.key_presser.updateSettings(settings)
        # Additional handling if needed

    def handleEmergencyStop(self):
        print("Emergency stop triggered!")
        # Stop any ongoing operations in the application
        self.mouse_clicker.stop_clicker()
        self.key_presser.stop_presser()

    def handleHideApp(self):
        print("Application hidden to tray.")
        self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainApp()
    sys.exit(app.exec_())
