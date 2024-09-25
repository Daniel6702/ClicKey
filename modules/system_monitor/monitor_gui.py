from base_components.base_gui import BaseGUI
from PyQt5.QtWidgets import QSizePolicy,QSpacerItem, QWidget, QVBoxLayout, QGroupBox, QGridLayout, QLabel, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, Qt

class MonitorGUI(BaseGUI):
    def __init__(self):
        super().__init__("System Monitor")
        self.memory_total = 0
        self.initClickerUI()

    def initClickerUI(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        self.title_widget.status_label.setText("")
        main_layout.addWidget(self.title_widget)

        # New GUI here
        # Create group boxes for each component
        self.create_cpu_group()
        self.create_gpu_group()
        self.create_memory_group()
        self.create_disk_group()
        self.create_network_group()
        self.create_battery_group()
        self.create_system_group()

        temp1_H = QHBoxLayout()
        temp1_H.addWidget(self.memory_group)
        temp1_H.addWidget(self.network_group)

        temp2_H = QHBoxLayout()
        temp2_H.addWidget(self.battery_group)
        temp2_H.addWidget(self.system_group)

        temp1_V = QVBoxLayout()
        temp1_V.addWidget(self.cpu_group)
        temp1_V.addWidget(self.gpu_group)

        temp3_H = QHBoxLayout()
        temp3_H.addLayout(temp1_V)
        temp3_H.addWidget(self.disk_group)

        main_layout.addLayout(temp3_H)
        main_layout.addLayout(temp1_H)
        main_layout.addLayout(temp2_H)

        self.setLayout(main_layout)

    # Create group boxes
    def create_cpu_group(self):
        self.cpu_group = QGroupBox("CPU")
        layout = QGridLayout()

        # CPU Labels
        self.cpu_model_label = QLabel("Model:")
        self.cpu_model_value = QLabel()
        self.cpu_usage_label = QLabel("Usage:")
        self.cpu_usage_value = QLabel()
        self.cpu_temp_label = QLabel("Temperature:")
        self.cpu_temp_value = QLabel()
        self.cpu_freq_label = QLabel("Frequency:")
        self.cpu_freq_value = QLabel()

        # Add widgets to layout
        layout.addWidget(self.cpu_model_label, 0, 0)
        layout.addWidget(self.cpu_model_value, 0, 1)
        layout.addWidget(self.cpu_usage_label, 1, 0)
        layout.addWidget(self.cpu_usage_value, 1, 1)
        layout.addWidget(self.cpu_temp_label, 2, 0)
        layout.addWidget(self.cpu_temp_value, 2, 1)
        layout.addWidget(self.cpu_freq_label, 3, 0)
        layout.addWidget(self.cpu_freq_value, 3, 1)

        self.cpu_group.setLayout(layout)

    def create_gpu_group(self):
        self.gpu_group = QGroupBox("GPU")
        layout = QGridLayout()

        # GPU Labels
        self.gpu_model_label = QLabel("Model:")
        self.gpu_model_value = QLabel()
        self.gpu_usage_label = QLabel("Usage:")
        self.gpu_usage_value = QLabel()
        self.gpu_temp_label = QLabel("Temperature:")
        self.gpu_temp_value = QLabel()
        self.gpu_mem_util_label = QLabel("Memory Utilization:")
        self.gpu_mem_util_value = QLabel()
        self.gpu_mem_freq_label = QLabel("Memory Frequency:")
        self.gpu_mem_freq_value = QLabel()
        self.gpu_core_freq_label = QLabel("Core Frequency:")
        self.gpu_core_freq_value = QLabel()

        # Add widgets to layout
        layout.addWidget(self.gpu_model_label, 0, 0)
        layout.addWidget(self.gpu_model_value, 0, 1)
        layout.addWidget(self.gpu_usage_label, 1, 0)
        layout.addWidget(self.gpu_usage_value, 1, 1)
        layout.addWidget(self.gpu_temp_label, 2, 0)
        layout.addWidget(self.gpu_temp_value, 2, 1)
        layout.addWidget(self.gpu_mem_util_label, 3, 0)
        layout.addWidget(self.gpu_mem_util_value, 3, 1)
        layout.addWidget(self.gpu_mem_freq_label, 4, 0)
        layout.addWidget(self.gpu_mem_freq_value, 4, 1)
        layout.addWidget(self.gpu_core_freq_label, 5, 0)
        layout.addWidget(self.gpu_core_freq_value, 5, 1)

        self.gpu_group.setLayout(layout)

    def create_memory_group(self):
        self.memory_group = QGroupBox("Memory")
        layout = QGridLayout()

        # Memory Labels
        self.memory_total_label = QLabel("Total:")
        self.memory_total_value = QLabel()
        self.memory_used_label = QLabel("Used:")
        self.memory_used_value = QLabel()
        self.memory_usage_label = QLabel("Usage:")
        self.memory_usage_value = QLabel()
        self.memory_speed_label = QLabel("Speed:")
        self.memory_speed_value = QLabel()

        # Add widgets to layout
        layout.addWidget(self.memory_total_label, 0, 0)
        layout.addWidget(self.memory_total_value, 0, 1)
        layout.addWidget(self.memory_used_label, 1, 0)
        layout.addWidget(self.memory_used_value, 1, 1)
        layout.addWidget(self.memory_usage_label, 2, 0)
        layout.addWidget(self.memory_usage_value, 2, 1)
        layout.addWidget(self.memory_speed_label, 3, 0)
        layout.addWidget(self.memory_speed_value, 3, 1)

        self.memory_group.setLayout(layout)

    def create_disk_group(self):
        self.disk_group = QGroupBox("Disks")
        layout = QVBoxLayout()

        # Disk Usage
        self.disk_usage_labels = {}  # Dictionary to hold labels for each disk
        self.disk_usage_values = {}
        # We'll dynamically add labels when disk info is received

        layout.addStretch()
        self.disk_group.setLayout(layout)

    def create_network_group(self):
        self.network_group = QGroupBox("Network")
        layout = QGridLayout()

        # Network Labels
        self.download_speed_label = QLabel("Download Speed:")
        self.download_speed_value = QLabel()
        self.upload_speed_label = QLabel("Upload Speed:")
        self.upload_speed_value = QLabel()

        # Add widgets to layout
        layout.addWidget(self.download_speed_label, 0, 0)
        layout.addWidget(self.download_speed_value, 0, 1)
        layout.addWidget(self.upload_speed_label, 1, 0)
        layout.addWidget(self.upload_speed_value, 1, 1)

        self.network_group.setLayout(layout)

    def create_battery_group(self):
        self.battery_group = QGroupBox("Battery")
        layout = QGridLayout()

        # Battery Labels
        self.battery_level_label = QLabel("Level:")
        self.battery_level_value = QLabel()
        self.battery_status_label = QLabel("Status:")
        self.battery_status_value = QLabel()

        # Add widgets to layout
        layout.addWidget(self.battery_level_label, 0, 0)
        layout.addWidget(self.battery_level_value, 0, 1)
        layout.addWidget(self.battery_status_label, 1, 0)
        layout.addWidget(self.battery_status_value, 1, 1)

        self.battery_group.setLayout(layout)

    def create_system_group(self):
        self.system_group = QGroupBox("System")
        layout = QGridLayout()

        # System Labels
        self.uptime_label = QLabel("Uptime:")
        self.uptime_value = QLabel()

        # Add widgets to layout
        layout.addWidget(self.uptime_label, 0, 0)
        layout.addWidget(self.uptime_value, 0, 1)

        self.system_group.setLayout(layout)

    # Slot methods to update GUI elements
    # CPU Slots
    def update_cpu_info(self, info):
        MAX_MODEL_LENGTH = 20
        model_name = info['model']
        if len(model_name) > MAX_MODEL_LENGTH:
            idx = model_name.rfind(' ', 0, MAX_MODEL_LENGTH)
            if idx == -1:
                idx = MAX_MODEL_LENGTH
            model_name = model_name[:idx].rstrip() + '\n' + model_name[idx:].lstrip()
        self.cpu_model_value.setText(model_name)
        self.cpu_freq_value.setText(f"{info['frequency']} MHz")

    def update_cpu_usage(self, usage):
        self.cpu_usage_value.setText(f"{usage}%")

    def update_cpu_temp(self, temp):
        self.cpu_temp_value.setText(f"{temp} °C")

    # GPU Slots
    def update_gpu_info(self, info):
        self.gpu_model_value.setText(info['name'])

    def update_gpu_usage(self, usage):
        self.gpu_usage_value.setText(f"{usage:.2f}%")

    def update_gpu_temp(self, temp):
        self.gpu_temp_value.setText(f"{temp} °C")

    def update_gpu_mem_util(self, mem_util):
        self.gpu_mem_util_value.setText(f"{mem_util:.2f}%")

    def update_gpu_mem_freq(self, mem_freq):
        self.gpu_mem_freq_value.setText(f"{mem_freq} MHz")

    def update_gpu_core_freq(self, core_freq):
        self.gpu_core_freq_value.setText(f"{core_freq} MHz")

    # Memory Slots
    def update_memory_info(self, info):
        self.memory_total = info['total']
        total_gb = info['total'] / (1024 ** 3)
        self.memory_total_value.setText(f"{total_gb:.2f} GB")
        if info['speed']:
            self.memory_speed_value.setText(f"{info['speed']} MHz")
        else:
            self.memory_speed_value.setText("Unknown")

    def update_memory_usage(self, usage_percent):
        self.memory_usage_value.setText(f"{usage_percent}%")
        used = self.memory_total * usage_percent / 100
        used_gb = used / (1024 ** 3)
        self.memory_used_value.setText(f"{used_gb:.2f} GB")

    def update_disk_info(self, info):
        layout = self.disk_group.layout()

        # Clear the existing layout if necessary
        if layout is None:
            layout = QVBoxLayout()
            self.disk_group.setLayout(layout)
        else:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

        # Rebuild the layout with top alignment
        layout.setAlignment(Qt.AlignTop)

        for partition in info['partitions']:
            label = QLabel(f"{partition} Usage:")
            value = QLabel()
            self.disk_usage_labels[partition] = label
            self.disk_usage_values[partition] = value
            
            h_layout = QHBoxLayout()
            h_layout.addWidget(label)
            h_layout.addWidget(value)
            
            layout.addLayout(h_layout)
        
        # Add a spacer to push everything upwards
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)

    def update_disk_usage(self, usage):
        for device, info in usage.items():
            percent = info['percent']
            if device in self.disk_usage_values:
                self.disk_usage_values[device].setText(f"{percent}%")

    # Network Slots
    def update_network_speed(self, download_speed, upload_speed):
        download_kb = download_speed / 1024
        upload_kb = upload_speed / 1024
        self.download_speed_value.setText(f"{download_kb:.2f} KB/s")
        self.upload_speed_value.setText(f"{upload_kb:.2f} KB/s")

    # Battery Slots
    def update_battery_status(self, status):
        self.battery_level_value.setText(f"{status['percent']}%")
        if status['power_plugged']:
            self.battery_status_value.setText("Charging")
        else:
            self.battery_status_value.setText("Discharging")

    # System Slots
    def update_system_uptime(self, uptime):
        hours = uptime / 3600
        self.uptime_value.setText(f"{hours:.2f} hours")

    def update_system_info(self, info):
        # You can add more system info here if needed
        pass
