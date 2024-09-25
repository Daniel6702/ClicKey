import cpuinfo
import psutil
import platform

class CPU:
    def __init__(self):
        self.model = cpuinfo.get_cpu_info()['brand_raw']
        self.cores_physical = psutil.cpu_count(logical=False)
        self.cores_logical = psutil.cpu_count(logical=True)
        self.frequency = psutil.cpu_freq().current

    def usage(self):
        return psutil.cpu_percent(interval=1)

    def temperature(self):
        # Try psutil's sensors_temperatures()
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                # Check for common keys
                for name in temps:
                    if name.lower() in ['coretemp', 'cpu_thermal', 'acpitz']:
                        entries = temps[name]
                        for entry in entries:
                            if entry.label in ('Package id 0', 'Tctl', 'Tdie'):
                                return entry.current
                        # Average core temperatures if no package temp is found
                        core_temps = [entry.current for entry in entries if "Core" in entry.label]
                        if core_temps:
                            return sum(core_temps) / len(core_temps)
                # Fallback to any temperature available
                for entries in temps.values():
                    for entry in entries:
                        return entry.current
        except Exception:
            pass

        # Use OpenHardwareMonitor on Windows
        if platform.system() == 'Windows':
            try:
                import clr
                import os
                dll_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'OpenHardwareMonitorLib.dll')
                clr.AddReference(dll_path)
                from OpenHardwareMonitor import Hardware

                computer = Hardware.Computer()
                computer.CPUEnabled = True
                computer.Open()

                for hw in computer.Hardware:
                    hw.Update()
                    for sensor in hw.Sensors:
                        if sensor.SensorType == Hardware.SensorType.Temperature and 'CPU' in sensor.Name:
                            if sensor.Value:
                                return sensor.Value
            except Exception:
                pass

            # Fallback to WMI
            try:
                import wmi
                w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
                sensors = w.Sensor()
                for sensor in sensors:
                    if sensor.SensorType == 'Temperature' and 'CPU' in sensor.Name:
                        if sensor.Value:
                            return sensor.Value
            except Exception:
                pass

            # Fallback to MSAcpi_ThermalZoneTemperature
            try:
                import wmi
                w = wmi.WMI(namespace="root\\WMI")
                temperature_info = w.MSAcpi_ThermalZoneTemperature()[0]
                temp = int(temperature_info.CurrentTemperature) / 10.0 - 273.15
                if temp:
                    return temp
            except Exception:
                pass

            try: 
                temp = psutil.sensors_temperatures()['coretemp'][0].current
                if temp:
                    return temp
            except Exception:
                pass

        # On Linux, read from thermal zones
        if platform.system() == 'Linux':
            try:
                import glob
                temps = []
                for sensor in glob.glob('/sys/class/thermal/thermal_zone*/temp'):
                    with open(sensor, 'r') as f:
                        temp = int(f.readline()) / 1000.0
                        temps.append(temp)
                if temps:
                    return sum(temps) / len(temps)
            except Exception:
                pass

        # On macOS, use osx-cpu-temp if available
        if platform.system() == 'Darwin':
            try:
                import subprocess
                temp_output = subprocess.check_output(["osx-cpu-temp"]).decode()
                temp = float(temp_output.strip().replace('°C', ''))
                return temp
            except Exception:
                pass

        # If all methods fail, return None
        return None


    def architecture(self):
        return platform.machine()

    def cache_size(self):
        return cpuinfo.get_cpu_info()['l3_cache_size']