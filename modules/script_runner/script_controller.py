from base_components.base_controller import BaseController
from modules.script_runner.script_logic import ScriptLogic
from modules.script_runner.script_gui import ScriptGUI

class ScriptController(BaseController):
    def __init__(self):
        super().__init__(ScriptLogic, ScriptGUI, 'default_settings/script_runner_settings.json')
        self.logic.update_script_signal.connect(self.gui.update_script)
        self.gui.start_recording_signal.connect(self.logic.start_recording)
        self.gui.stop_recording_signal.connect(self.logic.stop_recording)
        self.gui.save_script_signal.connect(self.logic.save_script)
        self.gui.load_script_signal.connect(self.logic.get_file_dialog)
        