from presser_logic import KeyPresserLogic
from presser_gui import KeyPresserGUI
from PyQt5.QtWidgets import QApplication
import sys

def apply_stylesheet(app: QApplication, path: str) -> None:
    with open(path, "r") as f:
        style = f.read()
        app.setStyleSheet(style)

class KeyPresserController():
    def __init__(self):
        self.logic = KeyPresserLogic(self.update_GUI)
        self.gui = KeyPresserGUI()

        self.gui.changeSettings.connect(self.logic.update_settings)
        self.gui.changeStatus.connect(self.logic.change_status)

        self.gui.show()
    
    def update_GUI(self):
        self.gui.update_GUI()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_stylesheet(app, "style.qss")
    controller = KeyPresserController()
    sys.exit(app.exec_())
