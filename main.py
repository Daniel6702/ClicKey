
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
from profiles.profiles_logic import ProfilesLogic
from profiles.profiles_gui import ProfilesGUI
from profiles.profiles_controller import ProfilesController
from color_tool.color_tool_logic import ColorLogic
from color_tool.color_tool_gui import ColorGUI

import sys
from PyQt5.QtWidgets import QApplication



def apply_stylesheet(app: QApplication, path: str) -> None:
    with open(path, "r") as f:
        style = f.read()
        app.setStyleSheet(style)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_stylesheet(app, "style.qss")
    color_controller = AutoActionController(ColorLogic, ColorGUI, "settings\\color_tool_settings.json", show=True)
    #mouse_controller = AutoActionController(ClickerLogic, ClickerGUI, "settings\\mouse_clicker_settings.json", show=False)
    #key_controller = AutoActionController(KeyPresserLogic, KeyPresserGUI, "settings\\key_presser_settings.json", show=False)
    #script_controller = ScriptController("settings\\script_runner_settings.json", show=False)
    #profiles_controller = ProfilesController([mouse_controller, key_controller, script_controller], 
    #                                         ["settings\\mouse_clicker_settings.json", "settings\\key_presser_settings.json", "settings\\script_runner_settings.json"])
    sys.exit(app.exec_())