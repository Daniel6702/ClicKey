from base_components.base_logic import BaseAutoActionLogic
import threading
import keyboard
'''
Updating hotkey: {'module': 'ClickerController', 'type': 'start', 'key': 'Ctrl+F1'}
Updating hotkey: {'module': 'ClickerController', 'type': 'stop', 'key': 'Ctrl+F2'} 
Updating hotkey: {'module': 'PresserController', 'type': 'start', 'key': 'Ctrl+F3'}
Updating hotkey: {'module': 'PresserController', 'type': 'stop', 'key': 'Ctrl+F4'} 
Updating hotkey: {'module': 'ScriptController', 'type': 'start', 'key': 'Ctrl+F5'} 
Updating hotkey: {'module': 'ScriptController', 'type': 'stop', 'key': 'Ctrl+F6'}
Updating hotkey: {'module': 'ColorController', 'type': 'lock', 'key': 'Ctrl+F7'}
Updating hotkey: {'module': 'ScriptController', 'type': 'script', 'key': 'Ctrl+F8'}
'''

class HotkeyLogic(BaseAutoActionLogic):
    def __init__(self):
        super().__init__()
        self.hotkeys = {} 
        self.active = True 
        self.listener_thread = threading.Thread(target=self.listen_for_hotkeys)
        self.listener_thread.daemon = True  
        self.listener_thread.start()  
        self.controllers = []

    def update_hotkey(self, hotkey_info: dict):
        """
        Updates the hotkey bindings with a new hotkey or changes an existing one.
        """
        key = hotkey_info['key']
        action = hotkey_info['type'] 
        module = hotkey_info['module']

        if key in self.hotkeys:
            keyboard.remove_hotkey(key)
            print(f"Removed existing hotkey: {key}")

        self.hotkeys[key] = (module, action)

        keyboard.add_hotkey(key, self.hotkey_triggered, args=(key,))
        print(f"Hotkey added: {key} for {module}.{action}")

    def hotkey_triggered(self, key):
        """
        This function is triggered when a hotkey is pressed.
        """
        if key in self.hotkeys:
            module, action = self.hotkeys[key]
            self.execute_hotkey(module, action)
            print(f"Hotkey pressed: {key}, triggering {module}.{action}")

    def execute_hotkey(self, module, action):
        for controller in self.controllers:
            #if controller.__class__.__name__ == module:
            if action == 'start':
                controller.gui.start()
                controller.logic.start()
            elif action == 'stop':
                controller.gui.stop()
                controller.logic.stop()
            elif action == 'script':
                controller.toggle_recording_button()
            elif action == 'lock':
                controller.toggle_lock()
            elif action.endswith('.txt'):
                controller.load_script(action)
            else:
                print(f"Invalid hotkey action: {action}")
                
    def listen_for_hotkeys(self):
        """
        Continuously listens for hotkeys in a separate thread.
        """
        while self.active:
            keyboard.wait()  

    def stop_listening(self):
        """
        Stops the hotkey listening thread.
        """
        self.active = False
        self.listener_thread.join() 