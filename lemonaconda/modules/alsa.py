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
import alsaaudio

VOLUME_REGEX = re.compile(b'\[(\d+)%\]\s*\[([a-z]+)\]')

class AlsaVolume(lemonaconda.Segment):
    def __init__(self, properties,
                 scontrol='Master', interval=5,
                 format_str='{vol_percent}',
                 ):
        super().__init__(properties)
        self.listener = AlsaListener(os.getpid(), scontrol, interval, format_str)
        self.process = threading.Thread(target=self.listener.execute,)

    def execute(self):
        self.process.start()

    def get_output(self):
        return self.listener.output

class AlsaListener(lemonaconda.Segment):
    def __init__(self, parentpid, scontrol, interval, format_str):
        self.parentpid = parentpid
        self.output = 'No valid data'
        self.scontrol = scontrol
        self.interval = interval
        self.format_str = format_str

    def execute(self):
        while True:
            output = subprocess.check_output(['amixer',
                                              'get', self.scontrol])
            matches = VOLUME_REGEX.findall(output)
            vol_percent = int(matches[0][0])
            state = matches[0][1].decode('utf-8')
            if state == 'off':
                vol_percent = 'MUTE'
            self.output = self.format_str.format(**{'vol_percent':vol_percent})
            time.sleep(self.interval)

