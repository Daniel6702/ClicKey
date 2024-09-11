import psutil

# CPU Information
print("CPU Count:", psutil.cpu_count(logical=True))  # Logical cores
print("Physical CPU Count:", psutil.cpu_count(logical=False))  # Physical cores
print("CPU Usage (%):", psutil.cpu_percent(interval=1))  # CPU usage

# Memory Information
memory_info = psutil.virtual_memory()
print("Total RAM (bytes):", memory_info.total)
print("Available RAM (bytes):", memory_info.available)
print("Memory Usage (%):", memory_info.percent)

# Disk Information
disk_info = psutil.disk_usage('/')
print("Total Disk Space (bytes):", disk_info.total)
print("Used Disk Space (bytes):", disk_info.used)
print("Disk Usage (%):", disk_info.percent)

import platform

print("System:", platform.system())
print("Node:", platform.node())
print("Release:", platform.release())
print("Version:", platform.version())
print("Machine:", platform.machine())
print("Processor:", platform.processor())

import cpuinfo

info = cpuinfo.get_cpu_info()
print("CPU Model:", info['brand_raw'])
print("Arch:", info['arch'])
print("Bits:", info['bits'])
print("Frequency (Hz):", info['hz_advertised_friendly'])
