# -*- coding: utf-8 -*-
import lemonaconda
import re
import subprocess
import threading
import os
import signal
import select
import alsaaudio

class AlsaVolume(lemonaconda.Segment):
    def __init__(self, properties, mixer='Master'):
        super().__init__(properties)
        self.listener = AlsaListener(os.getpid(), mixer)
        self.process = threading.Thread(target=self.listener.execute,)

    def execute(self):
        self.process.start()

    def get_output(self):
        # return '♫' + str(self.listener.output)
        return str(self.listener.output)

class AlsaListener(lemonaconda.Segment):
    def __init__(self, parentpid, mixer):
        self.parentpid = parentpid
        self.mixer = alsaaudio.Mixer(control=mixer)
        self.output = 'No valid data'

    def execute(self):
        self.output = self.mixer.getvolume()[0]
        fd, em = self.mixer.polldescriptors()[0]
        poller = select.poll()
        poller.register(fd, em)
        while True:
            # This will block forever
            events = poller.poll()
            for fd, flag in events:
                if flag == select.POLLIN:
                    # Leave result for the module to grab
                    # (Hopefully) shouldn't need locks, etc if only used in one place
                    self.output = self.mixer.getvolume()[0]
                    # # Send SIGUSR1 to redraw the bar
                    # os.kill(self.parentpid, signal.SIGUSR1)

