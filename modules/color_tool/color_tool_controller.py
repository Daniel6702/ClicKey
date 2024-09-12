from base_components.base_controller import BaseController
from modules.color_tool.color_tool_logic import ColorLogic
from modules.color_tool.color_tool_gui import ColorGUI

class ColorController(BaseController):
    def __init__(self):
        super().__init__(ColorLogic, ColorGUI, 'default_settings/color_tool_settings.json')