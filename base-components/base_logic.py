import threading
import json
import random
import platform

class BaseAutoActionLogic:
    def __init__(self, update_GUI):
        self.settings = self.load_json_settings()
        self.running = False
        self.stop_event = threading.Event()
        self.thread = None
        self.update_GUI = update_GUI

    def load_json_settings(self, file_path: str) -> dict:
        with open(file_path, 'r') as file:
            return json.load(file)

    def save_json_settings(self, settings, file_path: str):
        with open(file_path, 'w') as file:
            json.dump(settings, file, indent=4)

    def get_interval(self):
        if self.settings['random_interval']:
            min_delay = self.settings['min_delay']
            max_delay = self.settings['max_delay']
            return random.uniform(min_delay, max_delay)
        else:
            return self.settings['interval_norm']

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
        pass  # To be implemented by subclasses

    def play_beep(self):
        if platform.system() == "Windows":
            import winsound
            winsound.Beep(1000, 500)
        elif platform.system() == "Darwin":
            import os
            os.system('echo -n "\a"')