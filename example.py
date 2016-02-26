# -*- coding: utf-8 -*-
import lemonaconda
import lemonaconda.modules.render.powerlinish
import lemonaconda.modules.bspwm
import lemonaconda.modules.alsa
import lemonaconda.modules.weather_owm
import lemonaconda.modules.weather_yahoo

render = lemonaconda.modules.render.powerlinish.PowerlineRenderer()
panel = lemonaconda.Panel('181818', '181818', render, 1)

panel.add_segment(lemonaconda.modules.alsa.AlsaVolume(
    properties={'bgcolor':'afff00',
                'pl_left':False, 'pl_right': True,
                'alignment':'right',
                },
    interval = 2,
    format_str = '\u2009{icon}\u2009{vol_percent}',
), 'left')

panel.add_segment(lemonaconda.modules.bspwm.BspwmDesktops(
    properties={'bgcolor':'00afff',
                'pl_left':False, 'pl_right': True,
                'alignment':'left',
                'fgcolor_active': 'ffffff',
                'fgcolor_inactive': '181818',
                'fgcolor_urgent': 'ff0000',
                }
), 'left')

panel.add_segment(lemonaconda.ClockIndicator(
    properties={'bgcolor':'afff00',
                'pl_left':True, 'pl_right': False,
                'alignment':'right',
                }
), 'right')

panel.add_segment(lemonaconda.modules.weather_yahoo.WeatherYahoo(
    woeid='2400849',
    properties={'bgcolor':'00afff',
                'pl_left':True, 'pl_right': False,
                'alignment':'left',
                },
    format_str = '{icon} {temp_f}°F',
), 'right')

# panel.add_segment(lemonaconda.modules.weather_owm.WeatherOwm(
#     location='98203',
#     properties={'bgcolor':'00afff',
#                 'pl_left':True, 'pl_right': False,
#                 'alignment':'left',
#                 }
# ), 'right')

# panel.add_segment(lemonaconda.Segment(
#     properties={'bgcolor':'afff00',
#                 'pl_left':True, 'pl_right': True,
#                 }
# ))
panel.execute()
