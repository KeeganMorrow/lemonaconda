import statusbar
import re
import subprocess

class BspwmDesktops(statusbar.Segment):
    def execute(self):
        return
    def get_output(self):
        result = ''
        pattern = re.compile(r':([O,o,F,f,U,u])(\d)')
        status_b = subprocess.check_output(['bspc', 'control', '--get-status'])
        status = status_b.decode('utf-8')
        for (letter, num) in re.findall(pattern, status):
            if letter.lower() == 'u':
                result += ' %{{F#{fgcolor_urgent}}}{0} '.format(num,**self.properties)
            elif letter.isupper():
                result += ' %{{F#{fgcolor_active}}}{0} '.format(num,**self.properties)
            else:
                result += ' %{{F#{fgcolor_inactive}}}{0} '.format(num,**self.properties)
        result += ''
        return result

