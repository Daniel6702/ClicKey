import pyautogui
import json
import random
import threading
import platform
from collections import defaultdict
import time

def recursive_defaultdict():
    return defaultdict(recursive_defaultdict)

class ClickerLogic():
    def __init__(self, update_GUI):
        self.settings = self.load_json_settings()
        self.running = False
        self.stop_event = threading.Event()
        self.thread = None
        self.update_GUI = update_GUI

    def load_json_settings(self, file_path: str = 'mouse_clicker_settings.json') -> dict:
        with open(file_path, 'r') as file:
            return json.load(file)

    def save_json_settings(self, settings, file_path='mouse_clicker_settings.json'):
        with open(file_path, 'w') as file:
            json.dump(settings, file, indent=4)

    def perform_action(self, pos_x, pos_y):
        action = self.settings['action']
        action_settings = {
            "button": self.settings['button'],
            "x": pos_x,
            "y": pos_y         
        }
        if action == 'single_click':
            pyautogui.click(**action_settings)
        elif action == 'double_click':
            pyautogui.doubleClick(**action_settings)
        
        if self.settings.get('sound_effect'):
            threading.Thread(target=self.play_beep, daemon=True).start()

    def follow_mouse(self):
        pos = pyautogui.position()
        self.perform_action(pos.x, pos.y)

    def max_clicks_reached(self, clicks):
        if self.settings['click_inf']:
            return False
        print(f"clicks: {clicks}, click_times: {self.settings['click_times']}")
        return clicks >= self.settings['click_times']

    def center(self):
        screen_width, screen_height = pyautogui.size()
        self.perform_action(screen_width // 2, screen_height // 2)

    def random_position(self):
        screen_width, screen_height = pyautogui.size()
        random_x = random.randint(0, screen_width)
        random_y = random.randint(0, screen_height)
        self.perform_action(random_x, random_y)

    def coordinates(self):
        x = self.settings['x_pos']
        y = self.settings['y_pos']
        self.perform_action(x, y)

    def rectangle(self):
        rect_tl_x = self.settings['top_left_x_pos']
        rect_tl_y = self.settings['top_left_y_pos']
        rect_br_x = self.settings['bottom_right_x_pos']
        rect_br_y = self.settings['bottom_right_y_pos']
        random_x = random.randint(rect_tl_x, rect_br_x)
        random_y = random.randint(rect_tl_y, rect_br_y)
        self.perform_action(random_x, random_y)

    def get_interval(self):
        if self.settings['random_interval']:
            min_delay = self.settings['min_delay']
            max_delay = self.settings['max_delay']
            return random.uniform(min_delay, max_delay)
        else:
            return self.settings['interval_norm']

    def clicker(self):
        time.sleep(2)  # Initial delay
        clicks = 0
        position_mode = self.settings['position_mode']
        
        while self.running and not self.max_clicks_reached(clicks):
            if self.stop_event.is_set():
                break

            if position_mode == 'follow_mouse':
                self.follow_mouse()
            elif position_mode == 'center':
                self.center()
            elif position_mode == 'coordinates':
                self.coordinates()
            elif position_mode == 'random_position':
                self.random_position()
            elif position_mode == 'rectangle':
                self.rectangle()

            clicks += 1

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
            self.start_clicker()
        else:
            self.stop_clicker()

    def start_clicker(self):
        if self.running:
            return
        self.running = True
        self.stop_event.clear()
        self.thread = threading.Thread(target=self.clicker)
        self.thread.start()
        print("Clicker started.")

    def stop_clicker(self):
        if not self.running:
            return
        self.running = False
        self.stop_event.set()
        if self.thread is not None:
            self.thread.join()
        print("Clicker stopped.")

    def play_beep(self):
        if platform.system() == "Windows":
            import winsound
            winsound.Beep(1000, 500)
        elif platform.system() == "Darwin":
            import os
            os.system('echo -n "\a"')
