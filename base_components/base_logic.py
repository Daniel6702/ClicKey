import threading
import json
import random
import platform
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal

class BaseAutoActionLogic(QWidget):
    stop_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.running = False
        self.stop_event = threading.Event()
        self.thread = None

    def load_json_settings(self, file_path: str) -> dict:
        with open(file_path, 'r') as file:
            self.settings = json.load(file)
            return self.settings

    def get_interval(self):
        if self.settings.get('random_interval', False):
            min_delay = self.settings.get('min_delay', 0.1)
            max_delay = self.settings.get('max_delay', 1.0)
            return random.uniform(min_delay, max_delay)
        else:
            return self.settings.get('interval_norm', 1.0)
        
    def update_settings(self, new_settings: dict):
        for key, value in new_settings.items():
            if isinstance(value, dict):
                if key in self.settings:
                    self.settings[key].update(value)
                else:
                    self.settings[key] = value
            else:
                keys = key.split('.')
                d = self.settings
                for k in keys[:-1]:
                    d = d.setdefault(k, {})
                d[keys[-1]] = value

    def change_status(self, status: bool):
        if status:
            self.start()
        else:
            self.stop()

    def start(self):
        if self.running:
            return
        self.running = True
        self.stop_event.clear()
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def stop(self):
        if not self.running:
            return
        self.running = False
        self.stop_event.set()
        if self.thread is not None:
            self.thread.join()

    def run(self):
        raise NotImplementedError("Subclasses should implement this method")

    def play_beep(self):
        if platform.system() == "Windows":
            import winsound
            winsound.Beep(1000, 500)
        elif platform.system() == "Darwin":
            import os
            os.system('echo -n "\a"')
