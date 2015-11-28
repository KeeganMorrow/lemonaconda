import lemonaconda
import re
import subprocess
import multiprocessing
import os
import signal

class BspwmDesktops(lemonaconda.Segment):
    def __init__(self, properties):
        super().__init__(properties)
        self.pipe, listener_pipe = multiprocessing.Pipe()
        self.process = multiprocessing.Process(target=spawn_listener, args=(listener_pipe, os.getpid(),))
        self.cached_out = 'No valid data'

    def execute(self):
        print("starting listener")
        self.process.start()

    def get_output(self):
        if self.pipe.poll():
            self.cached_out = self.pipe.recv()
        return self.cached_out.format(**self.properties)

class BspcListener(lemonaconda.Segment):
    def __init__(self, pipe, parentpid):
        self.pipe = pipe
        self.parentpid = parentpid
        self.bspc = subprocess.Popen(['bspc', 'control', '--subscribe', 'report'], stdout = subprocess.PIPE)

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
            self.pipe.send(result)
            # Send SIGUSR1 to redraw the bar
            os.kill(self.parentpid, signal.SIGUSR1)

def spawn_listener(pipe, parentpid):
    listener = BspcListener(pipe, parentpid)
    listener.execute()

