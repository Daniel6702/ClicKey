import sys
from PyQt5.QtWidgets import QApplication
from module_manager.manager import CentralManagerGUI
from module_manager.utils import apply_stylesheet
from PyQt5.QtCore import Qt
import time
from default_settings import SETTINGS

if __name__ == "__main__":
    app = QApplication(sys.argv)
    SETTINGS.APP = app
    apply_stylesheet(app, f"styles\{SETTINGS.THEME}.qss")
    manager_window = CentralManagerGUI()
    SETTINGS.WINDOW = manager_window
    manager_window.move(app.desktop().screenGeometry().width()//2 - manager_window.width()//2, app.desktop().screenGeometry().height()//2 - manager_window.height()//2-100)
    manager_window.show()
    manager_window.load_modules()
    sys.exit(app.exec_())
