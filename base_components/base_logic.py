import threading
import json
import random
import platform

class BaseAutoActionLogic:
    def __init__(self, update_GUI, settings_file='settings.json'):
        self.settings = self.load_json_settings(settings_file)
        self.running = False
        self.stop_event = threading.Event()
        self.thread = None
        self.update_GUI = update_GUI

    def load_json_settings(self, file_path: str = 'settings.json') -> dict:
        with open(file_path, 'r') as file:
            return json.load(file)

    def save_json_settings(self, settings, file_path: str = 'settings.json'):
        with open(file_path, 'w') as file:
            json.dump(settings, file, indent=4)

    def get_interval(self):
        if self.settings.get('random_interval', False):
            min_delay = self.settings.get('min_delay', 0.1)
            max_delay = self.settings.get('max_delay', 1.0)
            return random.uniform(min_delay, max_delay)
        else:
            return self.settings.get('interval_norm', 1.0)
        
    def update_settings(self, new_settings: dict):
        print(new_settings)
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
