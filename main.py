
from key_presser.presser_logic import KeyPresserLogic
from key_presser.presser_gui import KeyPresserGUI
from mouse_clicker.clicker_logic import ClickerLogic
from mouse_clicker.clicker_gui import ClickerGUI
from script_runner.script_logic import ScriptLogic
from script_runner.script_gui import ScriptGUI
from base_components.controller import AutoActionController
from script_runner.script_controller import ScriptController
from script_runner.script_logic import ScriptLogic
from script_runner.script_gui import ScriptGUI

import sys
from PyQt5.QtWidgets import QApplication

def apply_stylesheet(app: QApplication, path: str) -> None:
    with open(path, "r") as f:
        style = f.read()
        app.setStyleSheet(style)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_stylesheet(app, "style.qss")
    controller = ScriptController("settings\\script_runner_settings.json")
    sys.exit(app.exec_())