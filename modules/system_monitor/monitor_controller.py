from base_components.base_controller import BaseController
from PyQt5.QtWidgets import QWidget
from modules.system_monitor.monitor_gui import MonitorGUI
from modules.system_monitor.monitor_logic import MonitorLogic

class SystemMonitorController(BaseController, QWidget):
    def __init__(self):
        super().__init__(MonitorLogic, MonitorGUI, 'default_settings/key_presser_settings.json')