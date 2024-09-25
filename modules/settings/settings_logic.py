from base_components.base_logic import BaseLogic
from default_settings import SETTINGS
from PyQt5.QtWidgets import QAction, QMenu, QSystemTrayIcon
from PyQt5.QtGui import QIcon
# Ensure you have imported these modules in your code

class SettingsLogic(BaseLogic):
    def __init__(self):
        super().__init__()
        self.tray_icon = None  # Initialize the tray icon variable
        self.hidden = False

    def hide_in_system_tray(self):
        """Set up the system tray icon and hide the main window."""
        window = SETTINGS.WINDOW  # Your main window instance
        window.hide()
        
        if self.hidden:
            return

        # Create the system tray icon
        self.tray_icon = QSystemTrayIcon(window)
        self.tray_icon.setIcon(QIcon("icon.jpg"))  # Replace with your tray icon path

        # Create context menu for the tray icon
        show_action = QAction("Show", window)
        hide_action = QAction("Hide", window)
        quit_action = QAction("Exit", window)

        show_action.triggered.connect(window.show)
        hide_action.triggered.connect(window.hide)
        quit_action.triggered.connect(SETTINGS.APP.quit)

        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)

        # Connect the activated signal
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

        # Show the tray icon
        self.tray_icon.show()

        # Override the closeEvent of the window
        window.closeEvent = self.closeEvent

        # Ensure the application keeps running after the window is closed
        SETTINGS.APP.setQuitOnLastWindowClosed(False)
        
        self.hidden = True

    def closeEvent(self, event):
        """Override the close event to minimize the app to the system tray."""
        event.ignore()
        SETTINGS.WINDOW.hide()
        self.tray_icon.showMessage(
            "Minimized to Tray",
            "The application is still running in the system tray.",
            QSystemTrayIcon.Information,
            2000  # Duration in milliseconds
        )

    def on_tray_icon_activated(self, reason):
        """Show the main window when the tray icon is clicked."""
        if reason == QSystemTrayIcon.Trigger:
            SETTINGS.WINDOW.show()

    def theme_changed(self, theme):
        SETTINGS.THEME = theme
        with open(f"styles\\{theme}.qss", "r") as f:
            style = f.read()
            SETTINGS.APP.setStyleSheet(style)

    def delay_changed(self, delay):
        SETTINGS.START_DELAY = delay