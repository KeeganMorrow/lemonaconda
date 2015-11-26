# -*- coding: utf-8 -*-

import time

class Panel:
    def __init__(self, bgcolor, fgcolor, renderer):
        self._segments = []
        self._renderer = renderer
        self._bgcolor = bgcolor
        self._fgcolor = fgcolor

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
        print(self._renderer.render(self))

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

