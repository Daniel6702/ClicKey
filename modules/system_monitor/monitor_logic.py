from base_components.base_logic import BaseLogic
import threading
import keyboard
from PyQt5.QtCore import pyqtSignal


from PyQt5.QtCore import QObject, pyqtSignal
import threading
import time
from modules.system_monitor.system_components.cpu import CPU
from modules.system_monitor.system_components.gpu import GPU
from modules.system_monitor.system_components.memory import Memory
from modules.system_monitor.system_components.disks import Disk
from modules.system_monitor.system_components.network import Network
from modules.system_monitor.system_components.battery import Battery
from modules.system_monitor.system_components.system import System

from PyQt5.QtCore import QObject, pyqtSignal
import threading
import time

class MonitorLogic(BaseLogic):
    # Signals for constant parameters
    cpu_info_signal = pyqtSignal(dict)
    gpu_info_signal = pyqtSignal(dict)
    memory_info_signal = pyqtSignal(dict)
    disk_info_signal = pyqtSignal(dict)
    system_info_signal = pyqtSignal(dict)

    # Signals for variable parameters
    cpu_usage_signal = pyqtSignal(float)
    cpu_temp_signal = pyqtSignal(float)
    gpu_usage_signal = pyqtSignal(float)
    gpu_temp_signal = pyqtSignal(float)
    gpu_mem_util_signal = pyqtSignal(float)
    gpu_mem_freq_signal = pyqtSignal(float)
    gpu_core_freq_signal = pyqtSignal(float)
    memory_usage_signal = pyqtSignal(float)
    disk_usage_signal = pyqtSignal(dict)
    network_speed_signal = pyqtSignal(float, float)  # download_speed, upload_speed
    battery_status_signal = pyqtSignal(object)
    system_uptime_signal = pyqtSignal(float)

    def __init__(self):
        super().__init__()

    def initialize(self):
        # Initialize threading events for synchronization
        self.cpu_event = threading.Event()
        self.gpu_event = threading.Event()
        self.memory_event = threading.Event()
        self.disk_event = threading.Event()
        self.network_event = threading.Event()
        self.battery_event = threading.Event()
        self.system_event = threading.Event()

        # Placeholders for monitor class instances
        self.cpu = None
        self.gpu = None
        self.memory = None
        self.disk = None
        self.network = None
        self.battery = None
        self.system = None

        # Start threads to initialize monitor classes
        threading.Thread(target=self.init_cpu, daemon=True).start()
        threading.Thread(target=self.init_gpu, daemon=True).start()
        threading.Thread(target=self.init_memory, daemon=True).start()
        threading.Thread(target=self.init_disk, daemon=True).start()
        threading.Thread(target=self.init_network, daemon=True).start()
        threading.Thread(target=self.init_battery, daemon=True).start()
        threading.Thread(target=self.init_system, daemon=True).start()

        # Start monitoring threads for variable parameters
        self.start_monitoring()

    # Initialization methods for monitor classes
    def init_cpu(self):
        self.cpu = CPU()
        self.cpu_event.set()  # Signal that CPU is initialized
        # Emit CPU constant parameters
        cpu_info = {
            'model': self.cpu.model,
            'cores_physical': self.cpu.cores_physical,
            'cores_logical': self.cpu.cores_logical,
            'frequency': self.cpu.frequency,
            'architecture': self.cpu.architecture(),
            'cache_size': self.cpu.cache_size()
        }
        self.cpu_info_signal.emit(cpu_info)

    def init_gpu(self):
        self.gpu = GPU()
        self.gpu_event.set()  # Signal that GPU is initialized
        if self.gpu.name:
            # Emit GPU constant parameters
            gpu_info = {
                'name': self.gpu.name,
                'memory_total': self.gpu.memory_total
            }
            self.gpu_info_signal.emit(gpu_info)

    def init_memory(self):
        self.memory = Memory()
        self.memory_event.set()  # Signal that Memory is initialized
        # Emit Memory constant parameters
        memory_info = {
            'total': self.memory.total,
            'speed': self.memory.speed
        }
        self.memory_info_signal.emit(memory_info)

    def init_disk(self):
        print(1)
        self.disk = Disk()
        print(2)
        self.disk_event.set()  # Signal that Disk is initialized
        # Emit Disk constant parameters
        disk_info = {
            'partitions': [partition.device for partition in self.disk.partitions]
        }
        print(f'Disk info1: {disk_info}')
        self.disk_info_signal.emit(disk_info)

    def init_network(self):
        self.network = Network()
        self.network_event.set()  # Signal that Network is initialized

    def init_battery(self):
        self.battery = Battery()
        self.battery_event.set()  # Signal that Battery is initialized

    def init_system(self):
        self.system = System()
        self.system_event.set()  # Signal that System is initialized
        # Emit System constant parameters
        system_info = {
            'boot_time': self.system.boot_time
        }
        self.system_info_signal.emit(system_info)

    def start_monitoring(self):
        """Start threads to periodically update variable parameters."""
        # CPU Usage
        threading.Thread(target=self.monitor_cpu_usage, daemon=True).start()
        # CPU Temperature
        threading.Thread(target=self.monitor_cpu_temp, daemon=True).start()
        # GPU Usage
        threading.Thread(target=self.monitor_gpu_usage, daemon=True).start()
        # GPU Temperature
        threading.Thread(target=self.monitor_gpu_temp, daemon=True).start()
        # GPU Memory Utilization
        threading.Thread(target=self.monitor_gpu_mem_util, daemon=True).start()
        # GPU Memory Frequency
        threading.Thread(target=self.monitor_gpu_mem_freq, daemon=True).start()
        # GPU Core Frequency
        threading.Thread(target=self.monitor_gpu_core_freq, daemon=True).start()
        # Memory Usage
        threading.Thread(target=self.monitor_memory_usage, daemon=True).start()
        # Disk Usage
        threading.Thread(target=self.monitor_disk_usage, daemon=True).start()
        # Network Speed
        threading.Thread(target=self.monitor_network_speed, daemon=True).start()
        # Battery Status
        threading.Thread(target=self.monitor_battery_status, daemon=True).start()
        # System Uptime
        threading.Thread(target=self.monitor_system_uptime, daemon=True).start()

    # Monitoring methods for variable parameters
    def monitor_cpu_usage(self):
        self.cpu_event.wait()  # Wait until CPU is initialized
        while True:
            usage = self.cpu.usage()
            self.cpu_usage_signal.emit(usage)
            time.sleep(1)  # Update every second

    def monitor_cpu_temp(self):
        self.cpu_event.wait()
        while True:
            temp = self.cpu.temperature()
            if temp is not None:
                self.cpu_temp_signal.emit(temp)
            time.sleep(2)  # Update every 2 seconds

    def monitor_gpu_usage(self):
        self.gpu_event.wait()
        while True:
            usage = self.gpu.usage()
            if usage is not None:
                self.gpu_usage_signal.emit(usage)
            time.sleep(1)

    def monitor_gpu_temp(self):
        self.gpu_event.wait()
        while True:
            temp = self.gpu.temperature()
            if temp is not None:
                self.gpu_temp_signal.emit(temp)
            time.sleep(2)

    def monitor_gpu_mem_util(self):
        self.gpu_event.wait()
        while True:
            mem_util = self.gpu.memory_utilization()
            if mem_util is not None:
                self.gpu_mem_util_signal.emit(mem_util)
            time.sleep(2)

    def monitor_gpu_mem_freq(self):
        self.gpu_event.wait()
        while True:
            mem_freq = self.gpu.memory_frequency()
            if mem_freq is not None:
                self.gpu_mem_freq_signal.emit(mem_freq)
            time.sleep(2)

    def monitor_gpu_core_freq(self):
        self.gpu_event.wait()
        while True:
            core_freq = self.gpu.core_frequency()
            if core_freq is not None:
                self.gpu_core_freq_signal.emit(core_freq)
            time.sleep(2)

    def monitor_memory_usage(self):
        self.memory_event.wait()
        while True:
            usage_percent = self.memory.usage_percent()
            self.memory_usage_signal.emit(usage_percent)
            time.sleep(1)

    def monitor_disk_usage(self):
        self.disk_event.wait()
        while True:
            usage = self.disk.usage()
            self.disk_usage_signal.emit(usage)
            time.sleep(5)

    def monitor_network_speed(self):
        self.network_event.wait()
        while True:
            download_speed = self.network.download_speed()
            upload_speed = self.network.upload_speed()
            self.network_speed_signal.emit(download_speed, upload_speed)
            time.sleep(1)

    def monitor_battery_status(self):
        self.battery_event.wait()
        while True:
            status = self.battery.status()
            if status is not None:
                self.battery_status_signal.emit(status)
            time.sleep(10)

    def monitor_system_uptime(self):
        self.system_event.wait()
        while True:
            uptime = self.system.uptime()
            self.system_uptime_signal.emit(uptime)
            time.sleep(10)
