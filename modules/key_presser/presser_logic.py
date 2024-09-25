from base_components.base_logic import BaseLogic
import pyautogui
import threading
import time
from default_settings.SETTINGS import START_DELAY

class KeyPresserLogic(BaseLogic):

    def run(self):
        time.sleep(START_DELAY)
        presses = 0
        repeat_inf = self.settings.get('repeat_inf', True)
        repeat_times = self.settings.get('repeat_times', 1)

        while self.running and (repeat_inf or presses < repeat_times):
            if self.stop_event.is_set():
                break

            self.perform_action()
            presses += 1

            interval = self.get_interval()
            print(f"Interval: {interval}")

            if not self.stop_event.wait(interval):
                continue

        self.stop_signal.emit()

    def perform_action(self):
        key = self.settings.get('key', 'a')
        combo_keys = []
        if self.settings.get('ctrl', False):
            combo_keys.append('ctrl')
        if self.settings.get('alt', False):
            combo_keys.append('alt')
        if self.settings.get('shift', False):
            combo_keys.append('shift')

        if combo_keys:
            pyautogui.hotkey(*combo_keys, key)
        else:
            pyautogui.press(key)

        if self.settings.get('sound_effect', False):
            threading.Thread(target=self.play_beep, daemon=True).start()
