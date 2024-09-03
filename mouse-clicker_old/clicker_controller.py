from clicker_logic import ClickerLogic
from clicker_gui import ClickerGUI
from PyQt5.QtWidgets import QApplication
import sys

def apply_stylesheet(app: QApplication, path: str) -> None:
    with open(path, "r") as f:
        style = f.read()
        app.setStyleSheet(style)

class ClickerController():
    def __init__(self):
        self.logic = ClickerLogic(self.update_GUI)
        self.gui = ClickerGUI()

        self.gui.changeSettings.connect(self.logic.update_settings)
        self.gui.changeStatus.connect(self.logic.change_status)

        self.gui.show()
    
    def update_GUI(self):
        self.gui.update_GUI()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_stylesheet(app, "style.qss")
    controller = ClickerController()
    sys.exit(app.exec_())