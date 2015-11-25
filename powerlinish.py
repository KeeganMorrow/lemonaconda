# -*- coding: utf-8 -*-
class Panel:
    def __init__(self, bgcolor):
        self._segments = []
        self._bgcolor = bgcolor

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
        string = ''
        for index, seg in enumerate(self._segments):
            string += '%{{B#{0}}}'.format(seg.color)
            if seg.leftarrow:
                if index > 0:
                    color = self._segments[index-1].color
                else:
                    color = self._bgcolor
                string += '%{{R}}%{{B#{0}}}%{{B-}}%{{R}}'.format(color)
            string += seg.text
            if seg.rightarrow:
                if index < len(self._segments) - 1:
                    color = self._segments[index+1].color
                else:
                    color = self._bgcolor
                string += '%{{R}}%{{B#{0}}}%{{B-}}%{{R}}'.format(color)
            string += '%{B-}'
        print(string)

class Segment:
    def __init__(self, alignment, color, text, leftarrow=False, rightarrow=False):
        self.panel = None
        self.alignment = alignment
        self.color = color
        self.text = text
        self.leftarrow = leftarrow
        self.rightarrow = rightarrow

panel = Panel('181818')
panel.add_segment(Segment('left', 'afff00', 'test segment 1', leftarrow=True))
panel.add_segment(Segment('left', '00afff', 'test segment 2', rightarrow=True))
panel.render()

