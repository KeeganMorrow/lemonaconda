# -*- coding: utf-8 -*-
import statusbar
import statusbar.modules.render.powerlinish

render = statusbar.modules.render.powerlinish.PowerlineRenderer()
panel = statusbar.Panel('181818', '181818', render)

panel.add_segment(statusbar.ClockIndicator(properties={'bgcolor':'afff00', 'pl_left':True, 'pl_right': False, 'alignment':'right'}))

# panel.add_segment(statusbar.Segment(properties={'bgcolor':'afff00', 'pl_left':True, 'pl_right': True}))
panel.render()
