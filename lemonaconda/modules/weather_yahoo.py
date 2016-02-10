import lemonaconda
import re
import subprocess
import threading
import os
import signal
import time
import urllib
import urllib.request
import urllib.parse
import json

YAHOO_BASE_WEATHER_URL = "https://query.yahooapis.com/v1/public/yql?"
# TODO('Make this configurable?')
YAHOO_QUERY_YQL = "select item.condition from weather.forecast where woeid = {woeid}"

class WeatherYahoo(lemonaconda.Segment):
    def __init__(self, properties, woeid, interval=120, format_str='{text} {temp_f}°'):
        super().__init__(properties)
        self.listener = WeatherYahooListener(woeid, interval, format_str)
        self.process = threading.Thread(target=self.listener.execute,)

    def execute(self):
        self.process.start()

    def get_output(self):
        return self.listener.output

class WeatherYahooListener(lemonaconda.Segment):
    def __init__(self, woeid, interval, format_str):
        self.output = 'No valid data'
        self.woeid = woeid
        self.interval = interval
        self.format_str = format_str

    def execute(self):
        while True:
            query = YAHOO_QUERY_YQL.format(woeid=self.woeid)
            yql_url = YAHOO_BASE_WEATHER_URL + urllib.parse.urlencode({'q':query}) + "&format=json"
            result = urllib.request.urlopen(yql_url).read().decode('utf-8')
            data = json.loads(result)
            condition = data['query']['results']['channel']['item']['condition']
            text = condition['text']
            if text == 'clouds':
                icon='c'
            elif text == 'clear':
                icon='f'
            elif text == 'snow':
                icon='☀'
            else:
                icon='?'
            temp_f = condition['temp']
            result = self.format_str.format(**{
                'icon':icon, 'temp_f':temp_f, 'text':text,})
            # Leave result for the module to grab
            # (Hopefully) shouldn't need locks, etc if only used in one place
            self.output = result
            # Send SIGUSR1 to redraw the bar
            # os.kill(self.parentpid, signal.SIGUSR1)
            time.sleep(self.interval)

def spawn_listener(parentpid):
    listener = BspcListener(parentpid)
    listener.execute()

