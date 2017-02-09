# -*- coding: utf-8 -*-
import lemonaconda
import re
import subprocess
import threading
import os
import signal
import time
import re
import select

VOLUME_REGEX = re.compile(b'\[(\d+)%\]\s*\[([a-z]+)\]')

# Note: Index zero is mute, others are evenly divided through volume percentage
default_volume_icons = [
    '\U0001f507',
    '\U0001f508',
    '\U0001f509',
    '\U0001f50a',
]

class AlsaVolume(lemonaconda.Segment):
    def __init__(self, properties,
        device=None,
        scontrol='Master', interval=5,
        format_str='{vol_percent}',
        icons = default_volume_icons
    ):
        super().__init__(properties)
        self.listener = AlsaListener(
            os.getpid(),
            device,
            scontrol,
            interval,
            format_str,
            icons
        )
        self.process = threading.Thread(
                target=self.listener.execute,
                daemon=True,
            )

    def execute(self):
        self.process.start()

    def get_output(self):
        return self.listener.output


class AlsaListener(lemonaconda.Segment):
    def __init__(
        self,
        parentpid,
        device,
        scontrol,
        interval,
        format_str,
        icons
    ):
        self.parentpid = parentpid
        self.output = 'No valid data'
        self.device = device
        self.scontrol = scontrol
        self.interval = interval
        self.format_str = format_str
        self.icons = icons

    def execute(self):
        while True:
            command = ['amixer']
            if self.device:
                command.append('-D')
                command.append(self.device)
            command.append('get')
            command.append(self.scontrol)
            output = subprocess.check_output(command)
            matches = VOLUME_REGEX.findall(output)
            vol_percent = int(matches[0][0])
            state = matches[0][1].decode('utf-8')

            if state == 'off':
                vol_percent = 'MUTE'
                icon = self.icons[0]
            else:
                vol_steps = len(self.icons) - 1
                step_size = 100 / vol_steps
                index = int(vol_percent / step_size)
                icon = self.icons[index]
            self.output = self.format_str.format(**{'vol_percent':vol_percent,
                                                    'icon': icon,
                                                    })
            time.sleep(self.interval)

