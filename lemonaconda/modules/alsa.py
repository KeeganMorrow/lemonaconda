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
    def __init__(self, properties, scontrol='Master', interval=5):
        super().__init__(properties)
        self.listener = AlsaListener(os.getpid(), scontrol, interval)
        self.process = threading.Thread(target=self.listener.execute,)

    def execute(self):
        self.process.start()

    def get_output(self):
        return '♫' + str(self.listener.output)
        # return str(self.listener.output)

class AlsaListener(lemonaconda.Segment):
    def __init__(self, parentpid, scontrol, interval):
        self.parentpid = parentpid
        self.output = 'No valid data'
        self.scontrol = scontrol
        self.interval = interval

    def execute(self):
        while True:
            output = subprocess.check_output(['amixer',
                                              'get', self.scontrol])
            matches = VOLUME_REGEX.findall(output)
            volume = int(matches[0][0])
            if str(matches[0][1]) == 'off':
                self.output = 'MUTE'
            else:
                self.output = '%s%%' % (volume)
            time.sleep(self.interval)

