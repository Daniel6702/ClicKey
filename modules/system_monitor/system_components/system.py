import psutil
import time

class System:
    def __init__(self):
        self.boot_time = psutil.boot_time()

    def uptime(self):
        return time.time() - self.boot_time