# -*- coding: utf-8 -*-

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
    def __init__(self, alignment, color, text, leftarrow=False, rightarrow=False):
        self.panel = None
        self.alignment = alignment
        self.color = color
        self.text = text
        self.leftarrow = leftarrow
        self.rightarrow = rightarrow

class Renderer:
    def render(self, panel):
        raise NotImplementedError("Method is abstract")
