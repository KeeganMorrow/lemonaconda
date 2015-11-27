# -*- coding: utf-8 -*-

import time
import sys
import re
import subprocess

class Panel:
    def __init__(self, bgcolor, fgcolor, renderer, interval):
        self._segments = []
        self._renderer = renderer
        self._bgcolor = bgcolor
        self._fgcolor = fgcolor
        self._interval = interval

    def add_segment(self, segment):
        self._segments.append(segment)
        segment.panel=self

    def get_next_segment(self, segment):
        lastseg = None
        for index, seg in enumerate(self._segments):
            if seg is segment:
                return self._segments[index+1]
            lastseg = seg
        # This should be an error

    def get_next_segment(self, segment):
        lastseg = None
        for seg in segments:
            if seg is segment:
                return lastseg
            lastseg = seg
        # This should be an error

    def render(self):
        result = self._renderer.render(self)
        print(result)
        sys.stdout.flush()

    def execute(self):
        while True:
            self.render()
            time.sleep(self._interval)

class Segment:
    def __init__(self, properties):
        self.panel = None
        self.properties = properties

    def execute(self):
        raise NotImplementedError("Method is abstract")

    def get_output(self):
        raise NotImplementedError("Method is abstract")

class ClockIndicator(Segment):
    def execute(self):
        return
    def get_output(self):
        return time.strftime("%a, %d %b %Y %H:%M:%S ", time.localtime())

class BspwmDesktops(Segment):
    def execute(self):
        return
    def get_output(self):
        result = ''
        pattern = re.compile(r':([O,o,F,f])(\d)')
        status_b = subprocess.check_output(['bspc', 'control', '--get-status'])
        status = status_b.decode('utf-8')
        for (letter, num) in re.findall(pattern, status):
            if letter.isupper():
                result += ' %{{F#{fgcolor_active}}}{0} '.format(num,**self.properties)
            else:
                result += ' %{{F#{fgcolor_inactive}}}{0} '.format(num,**self.properties)
        result += ''
        return result

class Renderer:
    def render(self, panel):
        raise NotImplementedError("Method is abstract")

