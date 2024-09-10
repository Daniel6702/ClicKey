from base_components.controller import AutoActionController
from modules.color_tool.color_tool_logic import ColorLogic
from modules.color_tool.color_tool_gui import ColorGUI

class ColorController(AutoActionController):
    def __init__(self):
        super().__init__(ColorLogic, ColorGUI, 'default_settings/color_tool_settings.json')