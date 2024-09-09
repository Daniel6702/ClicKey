import sys
from PyQt5.QtWidgets import QApplication
from module_manager.manager import CentralManagerGUI
from module_manager.manager import apply_stylesheet

if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, "style.qss")
    manager_window = CentralManagerGUI()
    manager_window.show()

    sys.exit(app.exec_())
