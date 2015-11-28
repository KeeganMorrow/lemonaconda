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
        t = time.time()
        while True:
            t += self._interval
            self.render()
            # Having the max() in here may only be neccessary
            # for windows
            time.sleep(max(0,t-time.time()))

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

class Renderer:
    def render(self, panel):
        raise NotImplementedError("Method is abstract")

