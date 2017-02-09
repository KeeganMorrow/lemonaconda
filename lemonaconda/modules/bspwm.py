import lemonaconda
import re
import subprocess
import threading
import os
import signal

class BspwmDesktops(lemonaconda.Segment):
    def __init__(self, properties):
        super().__init__(properties)
        self.listener = BspcListener(os.getpid())
        self.process = threading.Thread(
                target=self.listener.execute,
                daemon=True,
            )

    def execute(self):
        self.process.start()

    def get_output(self):
        return self.listener.output.format(**self.properties)

class BspcListener(lemonaconda.Segment):
    def __init__(self, parentpid):
        self.parentpid = parentpid
        self.bspc = subprocess.Popen(['bspc', 'subscribe', 'report'], stdout = subprocess.PIPE)
        self.output = 'No valid data'

    def execute(self):
        pattern = re.compile(r':([O,o,F,f,U,u])(\d)')
        while True:
            result = ''
            status_b = self.bspc.stdout.readline()
            status = status_b.decode('utf-8')
            for (letter, num) in re.findall(pattern, status):
                if letter.lower() == 'u':
                    result += ' %{{F#{fgcolor_urgent}}}' + '{0} '.format(num)
                elif letter.isupper():
                    result += ' %{{F#{fgcolor_active}}}' + '{0} '.format(num)
                else:
                    result += ' %{{F#{fgcolor_inactive}}}' + '{0} '.format(num)
            result += ''
            # Leave result for the module to grab
            # (Hopefully) shouldn't need locks, etc if only used in one place
            self.output = result
            # Send SIGUSR1 to redraw the bar
            os.kill(self.parentpid, signal.SIGUSR1)

def spawn_listener(parentpid):
    listener = BspcListener(parentpid)
    listener.execute()

