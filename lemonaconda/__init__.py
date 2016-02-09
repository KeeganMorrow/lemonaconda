# -*- coding: utf-8 -*-

import time
import sys
import re
import subprocess
import signal

class Panel:
    def __init__(self, bgcolor, fgcolor, renderer, interval):
        self._segments_left = []
        self._segments_right = []
        self._segments_center = []
        self._renderer = renderer
        self._bgcolor = bgcolor
        self._fgcolor = fgcolor
        self._interval = interval
        self._rendering = False

    def add_segment(self, segment, alignment):
        if alignment == 'left':
            self._segments_left.append(segment)
        elif alignment == 'right':
            self._segments_right.append(segment)
        elif alignment == 'center':
            self._segments_center.append(segment)
        else:
            raise(ValueError('Invalid alignment {0}'.format(alignment)))
        segment.panel=self

    def get_next_segment(self, segment):
        lastseg = None
        for index, seg in enumerate(self._segments):
            if seg is segment:
                return self._segments[index+1]
            lastseg = seg
        # This should be an error

    def render(self):
        if not self._rendering:
            self._rendering = True
            result = self._renderer.render(self)
            sys.stdout.write('%{S0}' + result)
            sys.stdout.write('%{S1}' + result + '\n')
            sys.stdout.flush()
            self._rendering = False

    def execute(self):
        signal.signal(signal.SIGUSR1, self.render_signal)
        segments = []
        segments.extend(self._segments_right)
        segments.extend(self._segments_center)
        segments.extend(self._segments_left)
        for seg in segments:
            seg.execute()
        while True:
            t = time.time() + self._interval
            self.render()
            # Having the max() in here may only be neccessary
            # for windows
            sleeptime = max(0,t-time.time())
            time.sleep(sleeptime)

    def render_signal(self, sig, frame):
        self.render()

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

