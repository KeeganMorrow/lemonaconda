# -*- coding: utf-8 -*-
import statusbar
import statusbar.modules.render.powerlinish

render = statusbar.modules.render.powerlinish.PowerlineRenderer()
panel = statusbar.Panel('181818', '181818', render)
panel.add_segment(statusbar.Segment('left', 'afff00', 'test segment 1', rightarrow=True))
panel.add_segment(statusbar.Segment('left', '00afff', 'test segment 2', rightarrow=True))
panel.render()
