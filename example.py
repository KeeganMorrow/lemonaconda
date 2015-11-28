# -*- coding: utf-8 -*-
import statusbar
import statusbar.modules.render.powerlinish
import statusbar.modules.bspwm

render = statusbar.modules.render.powerlinish.PowerlineRenderer()
panel = statusbar.Panel('181818', '181818', render, 0.25)

panel.add_segment(statusbar.ClockIndicator(properties={'bgcolor':'afff00', 'pl_left':True, 'pl_right': False, 'alignment':'right'}))

panel.add_segment(statusbar.modules.bspwm.BspwmDesktops(properties={'bgcolor':'00afff', 'pl_left':False, 'pl_right': True, 'alignment':'left', 'fgcolor_active': 'ffffff', 'fgcolor_inactive': '181818', 'fgcolor_urgent': 'ff0000'}))

# panel.add_segment(statusbar.Segment(properties={'bgcolor':'afff00', 'pl_left':True, 'pl_right': True}))
panel.execute()
