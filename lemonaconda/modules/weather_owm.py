import lemonaconda
import re
import subprocess
import threading
import os
import signal
import time
import pyowm

class WeatherOwm(lemonaconda.Segment):
    def __init__(self, properties, location, interval=120, format_str='{icon} {temp_f}'):
        super().__init__(properties)
        self.listener = WeatherOwmListener(location, interval, format_str)
        self.process = threading.Thread(target=self.listener.execute,)

    def execute(self):
        self.process.start()

    def get_output(self):
        return self.listener.output

class WeatherOwmListener(lemonaconda.Segment):
    def __init__(self, location, interval, format_str):
        self.output = 'No valid data'
        print(location)
        self.location = location
        self.interval = interval
        self.format_str = format_str

    def execute(self):
        owm = pyowm.OWM()
        observation = owm.weather_at_place(self.location)
        while True:
            w = observation.get_weather()
            w.get_wind()
            w.get_humidity()
            status = w.get_status()
            if status == 'clouds':
                icon='c'
            elif status == 'clear':
                icon='f'
            elif status == 'snow':
                icon='☀'
            else:
                icon='?'
            result = self.format_str.format(**{
                'icon':icon, 'temp_f':w.get_temperature(unit='fahrenheit')['temp']})
            # Leave result for the module to grab
            # (Hopefully) shouldn't need locks, etc if only used in one place
            self.output = result
            # Send SIGUSR1 to redraw the bar
            # os.kill(self.parentpid, signal.SIGUSR1)
            time.sleep(self.interval)

def spawn_listener(parentpid):
    listener = BspcListener(parentpid)
    listener.execute()

