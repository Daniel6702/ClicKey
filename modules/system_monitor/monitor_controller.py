from base_components.base_controller import BaseController
from PyQt5.QtWidgets import QWidget
from modules.system_monitor.monitor_gui import MonitorGUI
from modules.system_monitor.monitor_logic import MonitorLogic

class SystemMonitorController(BaseController, QWidget):
    def __init__(self):
        super().__init__(MonitorLogic, MonitorGUI, 'default_settings/place_holder.json')
        self.connect_signals()
        self.logic.initialize()

    def connect_signals(self):
        # Connect CPU signals
        self.logic.cpu_usage_signal.connect(self.gui.update_cpu_usage)
        self.logic.cpu_temp_signal.connect(self.gui.update_cpu_temp)
        self.logic.cpu_info_signal.connect(self.gui.update_cpu_info)
        # Connect GPU signals
        self.logic.gpu_usage_signal.connect(self.gui.update_gpu_usage)
        self.logic.gpu_temp_signal.connect(self.gui.update_gpu_temp)
        self.logic.gpu_mem_util_signal.connect(self.gui.update_gpu_mem_util)
        self.logic.gpu_mem_freq_signal.connect(self.gui.update_gpu_mem_freq)
        self.logic.gpu_core_freq_signal.connect(self.gui.update_gpu_core_freq)
        self.logic.gpu_info_signal.connect(self.gui.update_gpu_info)
        # Connect Memory signals
        self.logic.memory_usage_signal.connect(self.gui.update_memory_usage)
        self.logic.memory_info_signal.connect(self.gui.update_memory_info)
        # Connect Disk signals
        self.logic.disk_usage_signal.connect(self.gui.update_disk_usage)
        self.logic.disk_info_signal.connect(self.gui.update_disk_info)
        # Connect Network signals
        self.logic.network_speed_signal.connect(self.gui.update_network_speed)
        # Connect Battery signals
        self.logic.battery_status_signal.connect(self.gui.update_battery_status)
        # Connect System signals
        self.logic.system_uptime_signal.connect(self.gui.update_system_uptime)
        self.logic.system_info_signal.connect(self.gui.update_system_info)