from PyQt5.QtWidgets import QShortcut, QSystemTrayIcon, QMenu, QAction, QStyle, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QApplication, QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox, QSizePolicy
from PyQt5.QtGui import QKeySequence, QIcon
from PyQt5.QtCore import pyqtSignal, Qt
import sys

class Settings(QWidget):
    settingsChanged = pyqtSignal(dict)
    hideApp = pyqtSignal()
    showApp = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.default_settings = {
            'start_mouse_clicker_hotkey': 'Ctrl+Shift+M',
            'stop_mouse_clicker_hotkey': 'Ctrl+Shift+N',
            'start_key_presser_hotkey': 'Ctrl+Shift+K',
            'stop_key_presser_hotkey': 'Ctrl+Shift+L',
            'run_script_hotkey': 'Ctrl+Shift+R',
            'stop_script_hotkey': 'Ctrl+Shift+S',
            'toggle_overlay_hotkey': 'Ctrl+Shift+O',
        }
        self.settings = self.default_settings.copy()
        self.initUI()
        self.initTray()
    
    def get_default_settings(self):
        return self.default_settings.copy()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        self.title = QLabel("Hotkey Settings")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title)

        # Hotkeys Group
        hotkeys_group = QGroupBox("Hotkeys")
        hotkeys_layout = QVBoxLayout()
        hotkeys_group.setLayout(hotkeys_layout)
        hotkeys_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        # Hotkey Table
        self.hotkey_table = QTableWidget(7, 2)
        self.hotkey_table.setHorizontalHeaderLabels(["Hotkey", "Key"])
        self.hotkey_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.hotkey_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.hotkey_table.verticalHeader().setVisible(False)
        self.hotkey_table.setFixedHeight(self.hotkey_table.horizontalHeader().height() + 8 * self.hotkey_table.rowHeight(0))

        hotkeys = [
            ("Start Mouse Clicker", self.settings['start_mouse_clicker_hotkey']),
            ("Stop Mouse Clicker", self.settings['stop_mouse_clicker_hotkey']),
            ("Start Key Presser", self.settings['start_key_presser_hotkey']),
            ("Stop Key Presser", self.settings['stop_key_presser_hotkey']),
            ("Run Script", self.settings['run_script_hotkey']),
            ("Stop Script", self.settings['stop_script_hotkey']),
            ("Toggle Overlay", self.settings['toggle_overlay_hotkey'])
        ]

        for row, (name, key) in enumerate(hotkeys):
            self.hotkey_table.setItem(row, 0, QTableWidgetItem(name))
            key_item = QTableWidgetItem(key)
            key_item.setFlags(key_item.flags() | Qt.ItemIsEditable)
            self.hotkey_table.setItem(row, 1, key_item)

        self.hotkey_table.cellDoubleClicked.connect(self.on_hotkey_cell_double_clicked)
        hotkeys_layout.addWidget(self.hotkey_table)

        self.reset_button = QPushButton("Reset Hotkeys")
        self.reset_button.setObjectName("resetButton")
        self.reset_button.clicked.connect(self.reset_settings)
        hotkeys_layout.addWidget(self.reset_button)

        main_layout.addWidget(hotkeys_group)

        self.hide_button = QPushButton("Hide to Tray")
        self.hide_button.clicked.connect(self.hide_app)
        main_layout.addWidget(self.hide_button)
        
        self.setLayout(main_layout)

        # Apply CSS Styles
        self.applyStyles()

    def applyStyles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f9f9f9;
                font-family: Arial, sans-serif;
            }
            QLabel {
                font-size: 14px;
                color: #555;
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
            QLabel#title {
                font-size: 16px;
                color: #000000;
                font-weight: bold;
                margin-bottom: 10px;
                border: 1px solid #d3d3d3;
                border-radius: 5px;
                padding: 5px;
            }
            QTableWidget {
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
            QPushButton#resetButton {
                background-color: #ff9800;
                max-width: 100%;
            }
            QPushButton#resetButton:hover {
                background-color: #e68a00;
                max-width: 100%;
            }
            QPushButton#resetButton:pressed {
                background-color: #cc7a00;
                max-width: 100%;
            }
        """)

    def on_hotkey_cell_double_clicked(self, row, column):
        if column == 1:
            self.current_item = self.hotkey_table.item(row, column)
            self.grabKeyboard()

    def keyPressEvent(self, event):
        if hasattr(self, 'current_item') and self.current_item is not None:
            key_sequence = QKeySequence(event.key() + int(event.modifiers()))
            self.current_item.setText(key_sequence.toString())
            self.releaseKeyboard()
            self.current_item = None
            self.save_settings()  # Automatically save settings when a hotkey is changed

    def initTray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_ComputerIcon)))

        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)

        show_action.triggered.connect(self.showApp.emit)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(QApplication.instance().quit)

        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def save_settings(self):
        self.settings['start_mouse_clicker_hotkey'] = self.hotkey_table.item(0, 1).text()
        self.settings['stop_mouse_clicker_hotkey'] = self.hotkey_table.item(1, 1).text()
        self.settings['start_key_presser_hotkey'] = self.hotkey_table.item(2, 1).text()
        self.settings['stop_key_presser_hotkey'] = self.hotkey_table.item(3, 1).text()
        self.settings['run_script_hotkey'] = self.hotkey_table.item(4, 1).text()
        self.settings['stop_script_hotkey'] = self.hotkey_table.item(5, 1).text()
        self.settings['toggle_overlay_hotkey'] = self.hotkey_table.item(6, 1).text()
        self.settingsChanged.emit(self.settings)

    def reset_settings(self):
        self.settings = self.default_settings.copy()
        self.hotkey_table.item(0, 1).setText(self.settings['start_mouse_clicker_hotkey'])
        self.hotkey_table.item(1, 1).setText(self.settings['stop_mouse_clicker_hotkey'])
        self.hotkey_table.item(2, 1).setText(self.settings['start_key_presser_hotkey'])
        self.hotkey_table.item(3, 1).setText(self.settings['stop_key_presser_hotkey'])
        self.hotkey_table.item(4, 1).setText(self.settings['run_script_hotkey'])
        self.hotkey_table.item(5, 1).setText(self.settings['stop_script_hotkey'])
        self.hotkey_table.item(6, 1).setText(self.settings['toggle_overlay_hotkey'])
        self.settingsChanged.emit(self.settings)

    def get_settings(self):
        return {
            'start_mouse_clicker_hotkey': self.hotkey_table.item(0, 1).text(),
            'stop_mouse_clicker_hotkey': self.hotkey_table.item(1, 1).text(),
            'start_key_presser_hotkey': self.hotkey_table.item(2, 1).text(),
            'stop_key_presser_hotkey': self.hotkey_table.item(3, 1).text(),
            'run_script_hotkey': self.hotkey_table.item(4, 1).text(),
            'stop_script_hotkey': self.hotkey_table.item(5, 1).text(),
            'toggle_overlay_hotkey': self.hotkey_table.item(6, 1).text(),
        }

    def updateSettings(self, settings):
        self.hotkey_table.item(0, 1).setText(settings.get('start_mouse_clicker_hotkey', ''))
        self.hotkey_table.item(1, 1).setText(settings.get('stop_mouse_clicker_hotkey', ''))
        self.hotkey_table.item(2, 1).setText(settings.get('start_key_presser_hotkey', ''))
        self.hotkey_table.item(3, 1).setText(settings.get('stop_key_presser_hotkey', ''))
        self.hotkey_table.item(4, 1).setText(settings.get('run_script_hotkey', ''))
        self.hotkey_table.item(5, 1).setText(settings.get('stop_script_hotkey', ''))
        self.hotkey_table.item(6, 1).setText(settings.get('toggle_overlay_hotkey', ''))

    def get_default_settings(self):
        return self.default_settings.copy()

    def hide_app(self):
        self.hideApp.emit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Settings()
    ex.resize(400, 500)
    ex.settingsChanged.connect(lambda settings: print(f"Settings changed: {settings}"))
    ex.hideApp.connect(lambda: print("Application hidden to tray."))
    ex.show()
    sys.exit(app.exec_())
