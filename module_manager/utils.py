from PyQt5.QtWidgets import QApplication

from modules.mouse_clicker.mouse_clicker_controller import ClickerController
from modules.key_presser.key_presser_controller import PresserController
from modules.color_tool.color_tool_controller import ColorController
from modules.script_runner.script_controller import ScriptController
from modules.profile_manager.profiles_controller import ProfilesController
from modules.hotkey_manager.hotkey_controller import HotkeyController
from modules.settings.settings_controller import SettingsController
from modules.system_monitor.monitor_controller import SystemMonitorController

MODULES = {"Mouse Clicker": ClickerController, 
           "Key Presser": PresserController, 
           "Color Tool": ColorController, 
           "Script Runner": ScriptController, 
           "Profiles": ProfilesController,
           "Hotkeys": HotkeyController,
           "System Monitor": SystemMonitorController,
           "Settings": SettingsController}

def apply_stylesheet(app: QApplication, path: str) -> None:
    with open(path, "r") as f:
        style = f.read()
        app.setStyleSheet(style)