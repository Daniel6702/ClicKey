from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QGroupBox, QPushButton, QFileDialog, QFileDialog
from base_components.base_gui import BaseAutoActionGUI
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from modules.mouse_clicker.mouse_clicker_controller import ClickerController
from modules.key_presser.key_presser_controller import PresserController
from modules.script_runner.script_controller import ScriptController
from modules.color_tool.color_tool_controller import ColorController

class HotKey(QWidget):
    def __init__(self, label: str, key: str, module: str, type: str, signal: pyqtSignal = None):
        super().__init__()
        self.hot_key_changed = signal
        self.hot_key_changed.emit({'module': module, 'type': type, 'key': key})
        main_layout = QVBoxLayout()
        self.lock_color_label = QLabel(label)
        self.lock_color_input = QLineEdit()
        self.lock_color_input.setPlaceholderText(key)
        self.lock_color_input.textChanged.connect(lambda: self.hot_key_changed.emit({'module': module, 'type': type, 'key': self.lock_color_input.text()}))
        main_layout.addWidget(self.lock_color_label)
        main_layout.addWidget(self.lock_color_input)
        self.setLayout(main_layout)

class StartStopHotkeyWidget(QGroupBox):
    def __init__(self, module: str, name: str, start_key: str, stop_key: str, signal: pyqtSignal = None):
        super().__init__(name)  
        self.hot_key_changed = signal
        self.module = module
        self.initUI(start_key, stop_key)

    def initUI(self, start_key: str, stop_key: str):
        group_box_layout = QHBoxLayout()

        self.start_hotkey = HotKey("Start", start_key, self.module, 'start', self.hot_key_changed)
        self.stop_hotkey = HotKey("Stop", stop_key, self.module, 'stop', self.hot_key_changed)

        group_box_layout.addWidget(self.start_hotkey)
        group_box_layout.addWidget(self.stop_hotkey)

        self.setLayout(group_box_layout)

class RunScriptHotkeyWidget(QGroupBox):
    def __init__(self, name: str, signal: pyqtSignal = None):
        super().__init__(name)  
        self.hot_key_changed = signal
        self.initUI()

    def initUI(self):
        self.group_box_layout = QVBoxLayout()

        self.add_script_button = QPushButton("Add Script")
        self.add_script_button.clicked.connect(self.load_script)
        self.group_box_layout.addWidget(self.add_script_button)

        self.setLayout(self.group_box_layout)

    def load_script(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(None, "Load Script", "", "Text Files (*.txt);;All Files (*)", options=options)
        file_name = file_path.split('/')[-1]
        new_script_hotkey = HotKey(file_name, 'Ctrl+F9', ScriptController.__name__, file_path, self.hot_key_changed)
        self.group_box_layout.addWidget(new_script_hotkey)        

class HotkeyGUI(BaseAutoActionGUI):
    hot_key_changed = pyqtSignal(dict)

    def __init__(self):
        super().__init__("Hotkeys")

    def initClickerUI(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        self.title_widget.status_label.setText("")
        main_layout.addWidget(self.title_widget)

        mouse_clicker_widget = StartStopHotkeyWidget(ClickerController.__name__, 'Mouse Clicker', 'Ctrl+F1', 'Ctrl+F2', self.hot_key_changed)
        key_presser_widget = StartStopHotkeyWidget(PresserController.__name__, 'Key Presser', 'Ctrl+F3', 'Ctrl+F4', self.hot_key_changed)
        script_runner_widget = StartStopHotkeyWidget(ScriptController.__name__, 'Script Runner', 'Ctrl+F5', 'Ctrl+F6', self.hot_key_changed)

        misc_group_box = QGroupBox("Misc Hotkeys")
        misc_layout = QVBoxLayout()

        self.lock_color_hotkey = HotKey("Lock/Unlock Color", 'Ctrl+F7', ColorController.__name__, 'lock', self.hot_key_changed)
        self.start_stop_script_hotkey = HotKey("Start/Stop Script Recording", 'Ctrl+F8', ScriptController.__name__, 'script', self.hot_key_changed)

        misc_layout.addWidget(self.lock_color_hotkey)
        misc_layout.addWidget(self.start_stop_script_hotkey)

        run_script_on_hotkey_widget = RunScriptHotkeyWidget('Run Script on Hotkey', self.hot_key_changed)

        temp_H = QHBoxLayout()
        temp_H.addWidget(mouse_clicker_widget)
        temp_H.addWidget(key_presser_widget)
        temp_H.addWidget(script_runner_widget)
        main_layout.addLayout(temp_H)

        misc_group_box.setLayout(misc_layout)
        main_layout.addWidget(misc_group_box)
        main_layout.addWidget(run_script_on_hotkey_widget)

        self.setLayout(main_layout)