import platform
import GPUtil
import threading
import time

class GPU:
    def __init__(self, update_interval=5):
        self.update_interval = update_interval  
        gpus = GPUtil.getGPUs()
        if gpus:
            self.gpu = gpus[0]
            self.name = self.gpu.name
            self.memory_total = self.gpu.memoryTotal
            self.memory_used = self.gpu.memoryUsed
        else:
            self.gpu = None
            self.name = None
            self.memory_total = None
            self.memory_used = None

        self.update_thread = threading.Thread(target=self._update_gpu_info, daemon=True)
        self.update_thread.start()

    def _update_gpu_info(self):
        while True:
            gpus = GPUtil.getGPUs()
            self.gpu = gpus[0]
            self.memory_used = self.gpu.memoryUsed
            self.memory_total = self.gpu.memoryTotal
            time.sleep(self.update_interval)

    def usage(self):
        if self.gpu:
            return self.gpu.load * 100
        else:
            return None

    def temperature(self):
        if self.gpu:
            return self.gpu.temperature
        else:
            return None

    def memory_utilization(self):
        if self.gpu:
            return (self.memory_used / self.memory_total) * 100
        else:
            return None

    def memory_frequency(self):
        os_type = platform.system()
        if self.gpu is None:
            return None

        if os_type == 'Windows' or os_type == 'Linux':
            try:
                # Attempt to use NVIDIA Management Library (NVML)
                import pynvml
                pynvml.nvmlInit()
                handle = pynvml.nvmlDeviceGetHandleByIndex(self.gpu.id)
                mem_clock = pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_MEM)
                pynvml.nvmlShutdown()
                return mem_clock  # Returns memory clock frequency in MHz
            except ImportError:
                print("pynvml module is not installed. Please install it using 'pip install nvidia-ml-py3'.")
                return None
            except pynvml.NVMLError as e:
                print(f"An error occurred while retrieving memory frequency: {e}")
                return None
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                return None
        elif os_type == 'Darwin':
            # macOS does not have official NVML support
            return None
        else:
            return None
        
    def core_frequency(self):
        os_type = platform.system()
        if self.gpu is None:
            return None

        if os_type == 'Windows' or os_type == 'Linux':
            try:
                # Use NVIDIA Management Library (NVML)
                import pynvml
                pynvml.nvmlInit()
                handle = pynvml.nvmlDeviceGetHandleByIndex(self.gpu.id)
                core_clock = pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_GRAPHICS)
                pynvml.nvmlShutdown()
                return core_clock  # Core clock frequency in MHz
            except ImportError:
                print("pynvml module is not installed. Please install it using 'pip install nvidia-ml-py3'.")
                return None
            except pynvml.NVMLError as e:
                print(f"An error occurred while retrieving core frequency: {e}")
                return None
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                return None
        elif os_type == 'Darwin':
            # macOS does not have official NVML support
            return None
        else:
            return None