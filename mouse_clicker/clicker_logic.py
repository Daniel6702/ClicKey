import pyautogui
import random
import threading
import time
from base_components.base_logic import BaseAutoActionLogic

class ClickerLogic(BaseAutoActionLogic):
    def run(self):
        time.sleep(2)  # Initial delay
        clicks = 0
        position_mode = self.settings.get('position_mode', 'follow_mouse')
        click_inf = self.settings.get('repeat_inf', True)
        click_times = self.settings.get('repeat_times', 1)

        while self.running and (click_inf or clicks < click_times):
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

    def perform_action(self, pos_x=None, pos_y=None):
        action = self.settings.get('action', 'single_click')
        button = self.settings.get('button', 'left')

        if pos_x is None or pos_y is None:
            pos = pyautogui.position()
            pos_x, pos_y = pos.x, pos.y

        action_settings = {
            "button": button,
            "x": pos_x,
            "y": pos_y         
        }

        if action == 'single_click':
            pyautogui.click(**action_settings)
        elif action == 'double_click':
            pyautogui.doubleClick(**action_settings)
        
        if self.settings.get('sound_effect', False):
            threading.Thread(target=self.play_beep, daemon=True).start()

    def follow_mouse(self):
        pos = pyautogui.position()
        self.perform_action(pos.x, pos.y)

    def center(self):
        screen_width, screen_height = pyautogui.size()
        self.perform_action(screen_width // 2, screen_height // 2)

    def random_position(self):
        screen_width, screen_height = pyautogui.size()
        random_x = random.randint(0, screen_width)
        random_y = random.randint(0, screen_height)
        self.perform_action(random_x, random_y)

    def coordinates(self):
        x = self.settings.get('x_pos', 100)
        y = self.settings.get('y_pos', 100)
        self.perform_action(x, y)

    def rectangle(self):
        rect_tl_x = self.settings.get('top_left_x_pos', 0)
        rect_tl_y = self.settings.get('top_left_y_pos', 0)
        rect_br_x = self.settings.get('bottom_right_x_pos', 100)
        rect_br_y = self.settings.get('bottom_right_y_pos', 100)
        random_x = random.randint(rect_tl_x, rect_br_x)
        random_y = random.randint(rect_tl_y, rect_br_y)
        self.perform_action(random_x, random_y)
