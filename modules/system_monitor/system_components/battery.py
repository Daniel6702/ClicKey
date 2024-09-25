import psutil

class Battery:
    def __init__(self):
        pass

    def status(self):
        self.battery = psutil.sensors_battery()
        if self.battery:
            return {
                'percent': self.battery.percent,
                'time_left': self.battery.secsleft,
                'power_plugged': self.battery.power_plugged
            }
        else:
            return None