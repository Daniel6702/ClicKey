import psutil

class Disk:
    def __init__(self):
        self.partitions = psutil.disk_partitions()

    def usage(self):
        usage_info = {}
        for partition in self.partitions:
            usage = psutil.disk_usage(partition.mountpoint)
            usage_info[partition.device] = {
                'total': usage.total,
                'used': usage.used,
                'free': usage.free,
                'percent': usage.percent
            }
        return usage_info