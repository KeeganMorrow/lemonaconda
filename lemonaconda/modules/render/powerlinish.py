# -*- coding: utf-8 -*-

POWERLINE_ARROW_FORMAT = '%{{F#{bgcolor}}}%{{R}}{0}%{{R}}%{{F#{fgcolor}}}'

class PowerlineRenderer:
    def render(self, panel):
        string = '%{{F#{0}}}'.format(panel._fgcolor)
        string +='%{l}'
        string += self._render_section(panel, panel._segments_left)
        string +='%{c}'
        string += self._render_section(panel, panel._segments_center)
        string +='%{r}'
        string += self._render_section(panel, panel._segments_right)
        return string

    def _render_section(self, panel, section):
        string = ""
        for index, seg in enumerate(section):
            string += '%{{B#{0}}}'.format(seg.properties['bgcolor'])
            if seg.properties['pl_left']:
                if index > 0:
                    color = section[index-1].properties['bgcolor']
                else:
                    color = panel._bgcolor
                string += POWERLINE_ARROW_FORMAT.format('',
                                                        fgcolor=panel._fgcolor,
                                                        bgcolor=color,
                                                        )
            string += seg.get_output()
            if seg.properties['pl_right']:
                if index < len(section) - 1:
                    color = section[index+1].properties['bgcolor']
                else:
                    color = panel._bgcolor
                string += POWERLINE_ARROW_FORMAT.format('',
                                                        fgcolor=panel._fgcolor,
                                                        bgcolor=color,
                                                        )
            string += '%{B-}%{R}'
        return string

