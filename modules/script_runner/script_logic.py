import time
import pyautogui  # For mouse actions
import json
import threading
import keyboard  # For keyboard actions
from PyQt5.QtWidgets import QFileDialog
from base_components.base_logic import BaseAutoActionLogic
from pynput import mouse, keyboard
from PyQt5.QtCore import pyqtSignal

class ScriptLogic(BaseAutoActionLogic):
    update_script_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.recording = False
        self.record_delay = False  
        self.start_time = None  

        
        self.start_time = 0
        self.script = ""

    def on_press(self, key):
        '''
        Callback function for when a key is pressed. The key is passed to the new_action method to be added to the script.
        '''
        self.new_action({"type": "key_press", "key": key}, time.time())

    def on_click(self, x, y, button, pressed):
        '''
        Callback function for when a mouse button is clicked. The button and position are passed to the new_action method to be added to the script.
        '''
        if not pressed:
            return
        new_action = {}
        if button == mouse.Button.left:
            new_action = {"type": "mouse_click", "button": "left"}
        elif button == mouse.Button.right:
            new_action = {"type": "mouse_click", "button": "right"}
        elif button == mouse.Button.middle:
            new_action = {"type": "mouse_click", "button": "middle"}
        #"position_x": x, "position_y": y
        if self.settings.get('position', False):
            new_action = {**new_action, "position_x": x, "position_y": y}
        self.new_action(new_action, time.time())

    def new_action(self, action, time):
        '''
        Add a new action to the script. If the delay setting is on, the time between the current action and the previous action is calculated and added to the new action.
        '''
        delay_on = self.settings.get('delay', False)
        if delay_on:
            action["delay"] = round(time - self.start_time, 3)
            self.start_time = time
        print(f"New action: {action}")
        self.update_script_signal.emit(str(action))
        self.script += str(action) + '\n'

    def run(self):
        time.sleep(2) #Initial delay
        executions = 0
        repeat_inf = self.settings.get('repeat_inf', True)
        repeat_times = self.settings.get('repeat_times', 1)

        while self.running and (repeat_inf or executions < repeat_times):
            if self.stop_event.is_set():
                break

            self.execute_script()
            executions += 1

            interval = self.get_interval()

            if not self.stop_event.wait(interval):
                continue

        self.stop_signal.emit()

    def start_recording(self):
        print("Recording started")
        self.recording = True
        self.start_time = time.time()
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        self.mouse_listener.start()
        self.keyboard_listener.start()

    def stop_recording(self):
        print("Recording stopped")
        self.recording = False
        self.mouse_listener.stop()
        self.keyboard_listener.stop()

    def update_settings(self, new_settings: dict):
        super().update_settings(new_settings)
        if self.recording == False and new_settings.get('script_edit', False):
            self.script = new_settings.get('script_edit', "")

    def execute_action(self, action):
        """
        Executes a single action from the list.
        """
        action_type = action.get('type')

        if action_type == 'key_press':
            key = action.get('key')
            pyautogui.press(key)  # Simulates key press
            print(f"Key pressed: {key}")

        elif action_type == 'mouse_click':
            pos = pyautogui.position()
            position_x = action.get('position_x', pos.x)
            position_y = action.get('position_y', pos.y)
            button = action.get('button', 'left')
            pyautogui.click(x=position_x, y=position_y, button=button)
            print(f"Mouse clicked at: {(position_x, position_y)} with {button} button")

        else:
            print(f"Invalid action type: {action_type}")

    def execute_script(self):
        """
        Execute the recorded actions stored in the script, using threading to avoid blocking the GUI.
        """
        print(f'\nEXEUCTION STARTED')
        actions = []
        action = ""
        self.script += '\n'  # Add a newline to the end of the script to ensure the last action is added to the list
        for char in self.script:
            if char == '\n':
                actions.append(action)
                action = ""
            else:
                action += char

        converted_actions = []
        for action in actions:
            action = action.replace("'", "\"")
            try:
                action = json.loads(action)
                print(f'SUCCESSFULLY PARSED ACTION: {action}')
            except:
                print(f'FAILED TO PARSE ACTION: {action}')
                continue
            converted_actions.append(action)
        actions = converted_actions

        def execute_actions(actions):
            for action in actions:
                delay = action.get('delay', 0)
                time.sleep(delay)

                self.execute_action(action)

        execution_thread = threading.Thread(target=execute_actions, args=(actions,))
        execution_thread.start()

        print(f'EXECUTION FINISHED\n')

    def save_script(self, script):
        """
        Save the current script to a user-selected file using a file explorer.
        """
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(None, "Save Script", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as file:
                json.dump(self.script, file)

    def load_script(self):
        """
        Load the script from a user-selected file using a file explorer and populate the GUI.
        """
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(None, "Load Script", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'r') as file:
                    self.script = json.load(file)
                script_text = json.dumps(self.script, indent=4)
                self.update_script_signal.emit(script_text)
            except FileNotFoundError:
                print("No script file found.")

