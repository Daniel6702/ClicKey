import psutil
import time

class Network:
    def __init__(self):
        self.last_sent = psutil.net_io_counters().bytes_sent
        self.last_recv = psutil.net_io_counters().bytes_recv
        self.last_time = time.time()

    def download_speed(self):
        current_recv = psutil.net_io_counters().bytes_recv
        current_time = time.time()
        speed = (current_recv - self.last_recv) / (current_time - self.last_time)
        self.last_recv = current_recv
        self.last_time = current_time
        return speed  # Bytes per second

    def upload_speed(self):
        current_sent = psutil.net_io_counters().bytes_sent
        current_time = time.time()
        speed = (current_sent - self.last_sent) / (current_time - self.last_time)
        self.last_sent = current_sent
        self.last_time = current_time
        return speed  # Bytes per second
    
    def get_speeds(self):
        return self.download_speed(), self.upload_speed()