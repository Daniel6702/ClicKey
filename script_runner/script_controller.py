from base_components.controller import AutoActionController
from script_runner.script_logic import ScriptLogic
from script_runner.script_gui import ScriptGUI

class ScriptController(AutoActionController):
    def __init__(self, settings_file: str):
        # Call the base controller's initializer with the ScriptLogic and ScriptGUI
        super().__init__(ScriptLogic, ScriptGUI, settings_file)

        # Connect additional signals specific to script recording and execution
        self.gui.start_recording_signal.connect(self.logic.start_recording)
        self.gui.stop_recording_signal.connect(self.logic.stop_recording)
        self.gui.save_script_signal.connect(self.logic.save_script)
        self.gui.load_script_signal.connect(self.logic.load_script)
