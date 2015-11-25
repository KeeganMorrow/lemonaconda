# -*- coding: utf-8 -*-

POWERLINE_ARROW_FORMAT = '%{{F#{bgcolor}}}%{{R}}{0}%{{R}}%{{F#{fgcolor}}}'

class PowerlineRenderer:
    def render(self, panel):
        string = '%{{F#{0}}}'.format(panel._fgcolor)
        for index, seg in enumerate(panel._segments):
            string += '%{{B#{0}}}'.format(seg.color)
            if seg.leftarrow:
                if index > 0:
                    color = panel._segments[index-1].color
                else:
                    color = panel._bgcolor
                string += POWERLINE_ARROW_FORMAT.format('',
                                                        fgcolor=panel._fgcolor,
                                                        bgcolor=color,
                                                        )
            string += seg.text
            if seg.rightarrow:
                if index < len(panel._segments) - 1:
                    color = panel._segments[index+1].color
                else:
                    color = panel._bgcolor
                string += POWERLINE_ARROW_FORMAT.format('',
                                                        fgcolor=panel._fgcolor,
                                                        bgcolor=color,
                                                        )
            string += '%{B-}'
        print(string)

