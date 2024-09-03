import sys
import keyboard
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QLabel
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QUrl, QTimer, pyqtSignal
from PyQt5.QtGui import QDesktopServices

from mouse_clicker import MouseClicker
from KeyPresser.old import KeyPresser
from profiles import Profiles, ProfileManager
from scripts import Scripts
from settings import Settings

class MainApp(QWidget):
    toggleOverlaySignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.profile_manager = ProfileManager()
        self.current_button = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.adjustWindow)
        self.initUI()
        self.initConnections()
        self.hotkeys = self.settings.get_default_settings()
        self.hotkey_handlers = {} 
        self.setup_hotkeys()

    def adjustWindow(self):
        self.mouse_clicker.adjustSize()
        self.key_presser.adjustSize()

    def initUI(self):
        self.timer.start(0)

        def style_and_add_widget(widget, name):
            container = QWidget(self)
            container.setObjectName(name)
            layout = QVBoxLayout(container)
            layout.addWidget(widget)
            container.setStyleSheet(f"""
                #{name} {{
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    background-color: #f0f0f0;
                }}
            """)
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

        self.profiles = Profiles(self.profile_manager, self)  # Pass self to Profiles
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

    def restore_window(self):
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        self.show()
        self.raise_()
        self.activateWindow()

    def changePage(self, widget, button):
        self.stacked_widget.setCurrentWidget(widget)
        if self.current_button:
            self.current_button.setChecked(False)
        button.setChecked(True)
        self.current_button = button

    def initConnections(self):
        self.settings.settingsChanged.connect(self.handleHotkeyChange)
        self.settings.hideApp.connect(self.handleHideApp)
        self.settings.showApp.connect(self.restore_window)
        self.profiles.profileLoaded.connect(self.loadProfileSettings)

    def handleHotkeyChange(self, hotkeys):
        self.hotkeys = hotkeys
        self.setup_hotkeys()  # Re-setup hotkeys with new settings

    def handleHideApp(self):
        print("Application hidden to tray.")
        self.hide()

    def loadProfileSettings(self, settings):
        self.mouse_clicker.updateSettings(settings['mouse_clicker'])
        self.key_presser.updateSettings(settings['key_presser'])
        self.scripts.updateSettings(settings['scripts'])
        self.settings.updateSettings(settings['settings'])

    def openHelpPage(self):
        QDesktopServices.openUrl(QUrl("https://github.com/Daniel6702/ClicKey"))

    def setup_hotkeys(self):
        for hotkey, handler in self.hotkey_handlers.items():
            keyboard.remove_hotkey(handler)

        self.hotkey_handlers = {
            'start_mouse_clicker_hotkey': keyboard.add_hotkey(self.hotkeys['start_mouse_clicker_hotkey'], self.mouse_clicker.start_clicker),
            'stop_mouse_clicker_hotkey': keyboard.add_hotkey(self.hotkeys['stop_mouse_clicker_hotkey'], self.mouse_clicker.stop_clicker),
            'start_key_presser_hotkey': keyboard.add_hotkey(self.hotkeys['start_key_presser_hotkey'], self.key_presser.start_presser),
            'stop_key_presser_hotkey': keyboard.add_hotkey(self.hotkeys['stop_key_presser_hotkey'], self.key_presser.stop_presser),
            'run_script_hotkey': keyboard.add_hotkey(self.hotkeys['run_script_hotkey'], self.scripts.run_script),
            'stop_script_hotkey': keyboard.add_hotkey(self.hotkeys['stop_script_hotkey'], self.scripts.stop_script),
            'toggle_overlay_hotkey': keyboard.add_hotkey(self.hotkeys['toggle_overlay_hotkey'], self.toggleOverlay)
        }
    
    def toggleOverlay(self):
        self.toggleOverlaySignal.emit()

class Overlay(QWidget):
    toggleOverlaySignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()
        self.hide()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(100, 100, 400, 300)  # Adjust the size and position as needed

        layout = QVBoxLayout(self)

        overlay_label = QLabel("Overlay Window", self)
        overlay_label.setFont(QFont('Arial', 16))
        overlay_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(overlay_label)

        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.hide)
        layout.addWidget(close_button)

        self.setLayout(layout)

    def toggleOverlay(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainApp()

    # Create overlay window
    overlay_window = Overlay()

    # Connect signals
    main_window.toggleOverlaySignal.connect(overlay_window.toggleOverlay)

    sys.exit(app.exec_())
