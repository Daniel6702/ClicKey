import threading
import time
import json
import random
import pyautogui
import platform

class KeyPresserLogic:
    def __init__(self, update_GUI):
        self.settings = self.load_json_settings()
        self.running = False
        self.stop_event = threading.Event()
        self.thread = None
        self.update_GUI = update_GUI

    def load_json_settings(self, file_path: str = 'key_presser_settings.json') -> dict:
        with open(file_path, 'r') as file:
            return json.load(file)

    def save_json_settings(self, settings, file_path='key_presser_settings.json'):
        with open(file_path, 'w') as file:
            json.dump(settings, file, indent=4)

    def perform_action(self):
        key = self.settings['key']
        combo_keys = []
        if self.settings.get('ctrl'):
            combo_keys.append('ctrl')
        if self.settings.get('alt'):
            combo_keys.append('alt')
        if self.settings.get('shift'):
            combo_keys.append('shift')

        if combo_keys:
            pyautogui.hotkey(*combo_keys, key)
        else:
            pyautogui.press(key)

        if self.settings.get('sound_effect'):
            threading.Thread(target=self.play_beep, daemon=True).start()

    def max_presses_reached(self, presses):
        if self.settings['repeat_inf']:
            return False
        return presses >= self.settings['repeat_times']

    def get_interval(self):
        if self.settings['random_interval']:
            min_delay = self.settings['min_delay']
            max_delay = self.settings['max_delay']
            return random.uniform(min_delay, max_delay)
        else:
            return self.settings['interval_norm']

    def key_presser(self):
        time.sleep(2)  # Initial delay
        presses = 0

        while self.running and not self.max_presses_reached(presses):
            if self.stop_event.is_set():
                break

            self.perform_action()
            presses += 1

            interval = self.get_interval()

            if not self.stop_event.wait(interval):
                continue

        self.update_GUI()

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
            self.start_key_presser()
        else:
            self.stop_key_presser()

    def start_key_presser(self):
        if self.running:
            return
        self.running = True
        self.stop_event.clear()
        self.thread = threading.Thread(target=self.key_presser)
        self.thread.start()
        print("Key presser started.")

    def stop_key_presser(self):
        if not self.running:
            return
        self.running = False
        self.stop_event.set()
        if self.thread is not None:
            self.thread.join()
        print("Key presser stopped.")

    def play_beep(self):
        if platform.system() == "Windows":
            import winsound
            winsound.Beep(1000, 500)
        elif platform.system() == "Darwin":
            import os
            os.system('echo -n "\a"')
