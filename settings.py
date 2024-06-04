from PyQt5.QtWidgets import QShortcut, QSystemTrayIcon, QMenu, QAction, QStyle, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QApplication
from PyQt5.QtGui import QKeySequence, QIcon
from PyQt5.QtCore import pyqtSignal, Qt
import sys

class Settings(QWidget):
    settingsChanged = pyqtSignal(dict)
    emergencyStop = pyqtSignal()
    hideApp = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.default_settings = {
            'start_mouse_clicker_hotkey': 'Ctrl+Shift+M',
            'stop_mouse_clicker_hotkey': 'Ctrl+Shift+N',
            'start_key_presser_hotkey': 'Ctrl+Shift+K',
            'stop_key_presser_hotkey': 'Ctrl+Shift+L'
        }
        self.settings = self.default_settings.copy()
        self.initUI()
        self.initTray()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        layout.addWidget(QLabel("Hotkey Settings"))
        
        self.start_mouse_clicker_hotkey_input = QLineEdit(self.settings['start_mouse_clicker_hotkey'])
        self.stop_mouse_clicker_hotkey_input = QLineEdit(self.settings['stop_mouse_clicker_hotkey'])
        self.start_key_presser_hotkey_input = QLineEdit(self.settings['start_key_presser_hotkey'])
        self.stop_key_presser_hotkey_input = QLineEdit(self.settings['stop_key_presser_hotkey'])
        
        layout.addWidget(QLabel("Start Mouse Clicker Hotkey:"))
        layout.addWidget(self.start_mouse_clicker_hotkey_input)
        layout.addWidget(QLabel("Stop Mouse Clicker Hotkey:"))
        layout.addWidget(self.stop_mouse_clicker_hotkey_input)
        layout.addWidget(QLabel("Start Key Presser Hotkey:"))
        layout.addWidget(self.start_key_presser_hotkey_input)
        layout.addWidget(QLabel("Stop Key Presser Hotkey:"))
        layout.addWidget(self.stop_key_presser_hotkey_input)

        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)
        
        self.reset_button = QPushButton("Reset to Default")
        self.reset_button.clicked.connect(self.reset_settings)
        layout.addWidget(self.reset_button)

        self.emergency_button = QPushButton("Emergency Stop")
        self.emergency_button.clicked.connect(self.emergency_stop)
        layout.addWidget(self.emergency_button)

        self.hide_button = QPushButton("Hide to Tray")
        self.hide_button.clicked.connect(self.hide_app)
        layout.addWidget(self.hide_button)
        
        self.setLayout(layout)

    def initTray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_ComputerIcon)))

        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)

        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(QApplication.instance().quit)

        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def save_settings(self):
        self.settings['start_mouse_clicker_hotkey'] = self.start_mouse_clicker_hotkey_input.text()
        self.settings['stop_mouse_clicker_hotkey'] = self.stop_mouse_clicker_hotkey_input.text()
        self.settings['start_key_presser_hotkey'] = self.start_key_presser_hotkey_input.text()
        self.settings['stop_key_presser_hotkey'] = self.stop_key_presser_hotkey_input.text()
        self.settingsChanged.emit(self.settings)

    def reset_settings(self):
        self.settings = self.default_settings.copy()
        self.start_mouse_clicker_hotkey_input.setText(self.settings['start_mouse_clicker_hotkey'])
        self.stop_mouse_clicker_hotkey_input.setText(self.settings['stop_mouse_clicker_hotkey'])
        self.start_key_presser_hotkey_input.setText(self.settings['start_key_presser_hotkey'])
        self.stop_key_presser_hotkey_input.setText(self.settings['stop_key_presser_hotkey'])
        self.settingsChanged.emit(self.settings)

    def get_settings(self):
        return {
            'start_mouse_clicker_hotkey': self.start_mouse_clicker_hotkey_input.text(),
            'stop_mouse_clicker_hotkey': self.stop_mouse_clicker_hotkey_input.text(),
            'start_key_presser_hotkey': self.start_key_presser_hotkey_input.text(),
            'stop_key_presser_hotkey': self.stop_key_presser_hotkey_input.text(),
        }

    def updateSettings(self, settings):
        self.start_mouse_clicker_hotkey_input.setText(settings['start_mouse_clicker_hotkey'])
        self.stop_mouse_clicker_hotkey_input.setText(settings['stop_mouse_clicker_hotkey'])
        self.start_key_presser_hotkey_input.setText(settings['start_key_presser_hotkey'])
        self.stop_key_presser_hotkey_input.setText(settings['stop_key_presser_hotkey'])

    def get_default_settings(self):
        return {
            'start_mouse_clicker_hotkey': 'Ctrl+Shift+M',
            'stop_mouse_clicker_hotkey': 'Ctrl+Shift+N',
            'start_key_presser_hotkey': 'Ctrl+Shift+K',
            'stop_key_presser_hotkey': 'Ctrl+Shift+L',
        }

    def emergency_stop(self):
        self.emergencyStop.emit()

    def hide_app(self):
        self.hideApp.emit()
        self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Settings()
    ex.resize(400, 500)
    ex.settingsChanged.connect(lambda settings: print(f"Settings changed: {settings}"))
    ex.emergencyStop.connect(lambda: print("Emergency stop triggered!"))
    ex.hideApp.connect(lambda: print("Application hidden to tray."))
    ex.show()
    sys.exit(app.exec_())
