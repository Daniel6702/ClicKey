import psutil
import platform
import subprocess

class Memory:
    def __init__(self):
        self.total = psutil.virtual_memory().total
        self.speed = self.get_memory_speed()  # This is platform-dependent and may require external libraries

    def used(self):
        return psutil.virtual_memory().used

    def available(self):
        return psutil.virtual_memory().available

    def usage_percent(self):
        return psutil.virtual_memory().percent

    def get_memory_speed(self):
        os_type = platform.system()
        if os_type == 'Windows':
            try:
                import wmi
                c = wmi.WMI()
                mem_modules = c.Win32_PhysicalMemory()
                speeds = [int(module.Speed) for module in mem_modules if module.Speed is not None]
                if speeds:
                    return speeds[0]  # Returns a list of speeds for each memory module
                else:
                    return None
            except ImportError:
                print("wmi module is not installed. Please install it using 'pip install wmi'.")
                return None
            except Exception as e:
                print(f"An error occurred while retrieving memory speed on Windows: {e}")
                return None
        elif os_type == 'Linux':
            try:
                output = subprocess.check_output(['sudo', 'dmidecode', '-t', 'memory'], universal_newlines=True)
                speeds = []
                for line in output.split('\n'):
                    line = line.strip()
                    if line.startswith('Speed:'):
                        speed_str = line.split('Speed:')[-1].strip()
                        if speed_str != 'Unknown':
                            speed_value = speed_str.split(' ')[0]
                            if speed_value.isdigit():
                                speeds.append(int(speed_value))
                if speeds:
                    return speeds[0] 
                else:
                    return None
            except Exception as e:
                print(f"An error occurred while retrieving memory speed on Linux: {e}")
                return None
        elif os_type == 'Darwin':
            try:
                output = subprocess.check_output(['system_profiler', 'SPMemoryDataType'], universal_newlines=True)
                speeds = []
                for line in output.split('\n'):
                    line = line.strip()
                    if line.startswith('Speed:'):
                        speed_str = line.split('Speed:')[-1].strip()
                        if speed_str != 'N/A':
                            speed_value = speed_str.split(' ')[0]
                            if speed_value.isdigit():
                                speeds.append(int(speed_value))
                if speeds:
                    return speeds[0] 
                else:
                    return None
            except Exception as e:
                print(f"An error occurred while retrieving memory speed on macOS: {e}")
                return None
        else:
            return None