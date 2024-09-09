from base_components.controller import AutoActionController
from color_tool.color_tool_logic import ColorLogic
from color_tool.color_tool_gui import ColorGUI

class ColorController(AutoActionController):
    def __init__(self):
        super().__init__(ColorLogic, ColorGUI, 'settings/color_tool_settings.json')