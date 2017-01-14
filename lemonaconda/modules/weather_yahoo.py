# coding=utf-8
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

class WeatherYahooCodeEntry(object):
    def __init__(self, min_code, max_code, icon):
        self.min_code = min_code
        self.max_code = max_code
        self.icon = icon

    def match(self, code):
        if code <= self.max_code and code >= self.min_code:
            return True
        else:
            return False

DEFAULT_CODE_LOOKUP = [
    WeatherYahooCodeEntry(0, 0, '\U0001f32a'), #tornado
    WeatherYahooCodeEntry(1, 2, '\U0001f32a'), #tropical storm, hurricane
    WeatherYahooCodeEntry(3, 4, '\u26c8'), #thunderstorms, severe thunderstorms
    WeatherYahooCodeEntry(5, 7, '\u2744'), #mixed rain and snow, mixed rain and sleet, mixed snow and sleet
    WeatherYahooCodeEntry(8, 12, '\u2614'), #freezing drizzle, drizzle, freezing rain, showers
    WeatherYahooCodeEntry(13, 16, '\u2744'), #snow flurries, light snow showers, blowing snow, snow
    WeatherYahooCodeEntry(17, 18, '\u26c8'), #hail, sleet
    WeatherYahooCodeEntry(19, 16, '\u2601'), #dust
    WeatherYahooCodeEntry(20, 21, '\u2601'), #foggy, haze
    WeatherYahooCodeEntry(22, 22, '\u2601'), #smokey
    WeatherYahooCodeEntry(23, 24, '\U0001f32c'), #blustery, windy
    WeatherYahooCodeEntry(25, 25, '\u263c'), #cold
    WeatherYahooCodeEntry(26, 30, '\u2601'), #cloudy, mostly cloudy, partly cloudy
    WeatherYahooCodeEntry(31, 31, '\u263d'), #clear (night?)
    WeatherYahooCodeEntry(32, 32, '\u263c'), #sunny
    WeatherYahooCodeEntry(33, 34, '\u263c'), #fair
    WeatherYahooCodeEntry(35, 35, '\2744'), #mixed rain and hail
    WeatherYahooCodeEntry(36, 36, '\u2600'), #hot
    WeatherYahooCodeEntry(37, 39, '\u26c8'), #isolated, scattered thunderstorms
    WeatherYahooCodeEntry(41, 43, '\u2744'), #heavy snow, scattered snow showers, heavy snow
    WeatherYahooCodeEntry(44, 44, '\u2601'), #partly cloudy
    WeatherYahooCodeEntry(45, 45, '\u26c8'), #thundershowers
    WeatherYahooCodeEntry(46, 46, '\u2744'), #snow showers
    WeatherYahooCodeEntry(47, 47, '\u26c8'), #isolated thundershowers
]

class WeatherYahoo(lemonaconda.Segment):
    def __init__(self, properties, woeid, interval=120, format_str='{icon} {text} {temp_f}°', code_lookup=DEFAULT_CODE_LOOKUP):
        super().__init__(properties)
        self.listener = WeatherYahooListener(woeid, interval,
                                             format_str, code_lookup
                                             )
        self.process = threading.Thread(target=self.listener.execute,)

    def execute(self):
        self.process.start()

    def get_output(self):
        return self.listener.output

class WeatherYahooListener(lemonaconda.Segment):
    def __init__(self, woeid, interval, format_str, code_lookup):
        self.output = 'No valid data'
        self.woeid = woeid
        self.interval = interval
        self.format_str = format_str
        self.code_lookup = code_lookup

    def execute(self):
        while True:
            query = YAHOO_QUERY_YQL.format(woeid=self.woeid)
            yql_url = YAHOO_BASE_WEATHER_URL + urllib.parse.urlencode({'q':query}) + "&format=json"
            result = urllib.request.urlopen(yql_url).read().decode('utf-8')
            data = json.loads(result)
            condition = data['query']['results']['channel']['item']['condition']
            text = condition['text']
            code = int(condition['code'])
            icon = '?'
            for entry in self.code_lookup:
                if entry.match(code):
                    icon = entry.icon
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

