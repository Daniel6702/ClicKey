import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QLabel
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtGui import QDesktopServices

from mouse_clicker import MouseClicker
from key_presser import KeyPresser
from profiles import Profiles, ProfileManager
from scripts import Scripts
from settings import Settings

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.profile_manager = ProfileManager()
        self.current_button = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.adjustWindow)
        self.initUI()
        self.initConnections()

    def adjustWindow(self):
        self.mouse_clicker.adjustSize()
        #self.adjustSize()

    def initUI(self):
        self.timer.start(1)
        def style_and_add_widget(widget, name):
            container = QWidget(self)
            container.setObjectName(name)
            layout = QVBoxLayout(container)
            layout.addWidget(widget)
            container.setStyleSheet("""
                #{name} {{
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    background-color: #f0f0f0;
                }}
            """.format(name=name))
            self.stacked_widget.addWidget(container)
            return container

        main_layout = QHBoxLayout()
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setAlignment(Qt.AlignTop)

        self.stacked_widget = QStackedWidget(self)

        self.mouse_clicker = MouseClicker()
        mouse_clicker_container = style_and_add_widget(self.mouse_clicker, "MouseClickerContainer")

        self.key_presser = KeyPresser()
        key_presser_container = style_and_add_widget(self.key_presser, "KeyPresserContainer")

        self.profiles = Profiles(self.profile_manager)
        profiles_container = style_and_add_widget(self.profiles, "ProfilesContainer")

        self.scripts = Scripts()
        scripts_container = style_and_add_widget(self.scripts, "ScriptsContainer")

        self.settings = Settings()
        settings_container = style_and_add_widget(self.settings, "SettingsContainer")

        app_name_label = QLabel("ClicKey", self)
        app_name_label.setObjectName("AppLabel")
        app_name_label.setFont(QFont('Arial', 16))
        app_name_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(app_name_label)

        self.buttons = [
            ("Mouse Clicker", mouse_clicker_container),
            ("Key Presser", key_presser_container),
            ("Scripts", scripts_container),
            ("Profiles", profiles_container),
            ("Settings", settings_container)
        ]

        for i, (name, container) in enumerate(self.buttons):
            button = QPushButton(name, self)
            button.setCheckable(True)
            button.setObjectName("Button")
            button.clicked.connect(lambda _, c=container, b=button: self.changePage(c, b))
            sidebar_layout.addWidget(button)

            if i == 0:  # Set the first button as active initially
                button.setChecked(True)
                self.current_button = button
                self.stacked_widget.setCurrentWidget(container)

        help_button = QPushButton("Help")
        help_button.setObjectName("Button")
        help_button.setIcon(QIcon("help_icon.png"))  # Use your help icon path here
        help_button.clicked.connect(self.openHelpPage)
        sidebar_layout.addWidget(help_button)

        main_layout.addLayout(sidebar_layout)
        main_layout.addWidget(self.stacked_widget)

        self.setLayout(main_layout)
        self.setWindowTitle('ClicKey')
        self.resize(500, 600)
        self.applyStyles()
        self.show()

    def applyStyles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;          
            }
            QLabel#AppLabel {
                font-size: 30px;
                font-weight: bold;
                color: #333;
                padding: 10px;
                text-align: center;
            }
            QPushButton#Button {
                font-size: 16px;
                color: #333;
                background-color: #fff;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px 20px;
                margin: 5px 0;
            }
            QPushButton#Button:hover {
                background-color: #e0e0e0;
            }
            QPushButton#Button:checked {
                background-color: #0078d7;
                color: #fff;
                border: none;
            }
            QPushButton#Button:focus {
                outline: none;
            }
        """)

    def changePage(self, widget, button):
        self.stacked_widget.setCurrentWidget(widget)
        if self.current_button:
            self.current_button.setChecked(False)
        button.setChecked(True)
        self.current_button = button

    def initConnections(self):
        self.settings.settingsChanged.connect(self.handleSettingsChanged)
        self.settings.emergencyStop.connect(self.handleEmergencyStop)
        self.settings.hideApp.connect(self.handleHideApp)
        self.profiles.profileLoaded.connect(self.loadProfileSettings)

    def handleSettingsChanged(self, settings):
        print(f"Settings changed: {settings}")
        self.mouse_clicker.updateSettings(settings)
        self.key_presser.updateSettings(settings)
        self.settings.updateSettings(settings)

    def handleEmergencyStop(self):
        print("Emergency stop triggered!")
        self.mouse_clicker.stop_clicker()
        self.key_presser.stop_presser()

    def handleHideApp(self):
        print("Application hidden to tray.")
        self.hide()

    def loadProfileSettings(self, settings):
        self.mouse_clicker.updateSettings(settings['mouse_clicker'])
        self.key_presser.updateSettings(settings['key_presser'])
        self.scripts.updateSettings(settings['scripts'])
        self.settings.updateSettings(settings['settings'])

    def openHelpPage(self):
        QDesktopServices.openUrl(QUrl("https://github.com/Daniel6702/AutoClicker"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainApp()
    sys.exit(app.exec_())
