import time
import pyautogui  # For mouse actions
import json
import threading
import keyboard  # For keyboard actions
from PyQt5.QtWidgets import QFileDialog
from base_components.base_logic import BaseAutoActionLogic
from pynput import mouse, keyboard


class ScriptLogic(BaseAutoActionLogic):
    def __init__(self, update_GUI, settings_file='settings.json'):
        super().__init__(update_GUI, settings_file)
        self.actions = []  
        self.recording = False
        self.record_delay = False  
        self.start_time = None  

        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        self.start_time = 0

    def on_press(self, key):
        self.new_action({"type": "key_press", "key": key}, time.time())

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.left and pressed:
            self.new_action({"type": "mouse_click", "position": (x, y), "button": "left"}, time.time())
        elif button == mouse.Button.right and pressed:
            self.new_action({"type": "mouse_click", "position": (x, y), "button": "right"}, time.time())
        elif button == mouse.Button.middle and pressed:
            self.new_action({"type": "mouse_click", "position": (x, y), "button": "middle"}, time.time())

    def new_action(self, action, time):
        delay_on = self.settings.get('delay', False)
        if delay_on:
            action["delay"] = round(time - self.start_time, 3)
            self.start_time = time
        self.actions.append(action)
        self.update_GUI(load_script=True, script=action)
        print(self.actions)

    def run(self):
        self.execute_script()

    def start_recording(self):
        self.actions = []
        self.recording = True
        self.start_time = time.time()
        self.mouse_listener.start()
        self.keyboard_listener.start()

    def stop_recording(self):
        self.recording = False
        self.mouse_listener.stop()
        self.keyboard_listener.stop()

    def update_settings(self, new_settings: dict):
        super().update_settings(new_settings)
        if self.recording == False and new_settings.get('script_edit', False) and new_settings.get('changed_lines', 0) > 0:
            action_changed = new_settings.get('changed_lines', 0)
            try:
                self.actions[action_changed] = json.loads(new_settings.get('script_edit').replace("'", '"'))
            except json.JSONDecodeError:
                print("Invalid Command")
            else:
                print(f"COMMAND CHANGED {new_settings.get('script_edit')} TYPE: {type(new_settings.get('script_edit'))}")

            print(self.actions)

    def execute_script(self):
        """
        Execute the recorded actions stored in the script.
        """
        for action in self.actions:
            if action["type"] == "mouse_click":
                pyautogui.click(x=action["position"][0], y=action["position"][1])
            elif action["type"] == "key_press":
                pyautogui.press(action["key"])

            if "delay" in action and self.record_delay:
                time.sleep(action["delay"])

    def save_script(self, script):
        """
        Save the current script to a user-selected file using a file explorer.
        """
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(None, "Save Script", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as file:
                json.dump(self.actions, file)

    def load_script(self):
        """
        Load the script from a user-selected file using a file explorer and populate the GUI.
        """
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(None, "Load Script", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'r') as file:
                    self.actions = json.load(file)
                script_text = json.dumps(self.actions, indent=4)
                self.update_GUI(script_text)
            except FileNotFoundError:
                print("No script file found.")

