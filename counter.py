#! /usr/bin/env python
# -*-coding:utf-8 -*

import sys
from time import sleep
from termcolor import colored

class Counter(object):
    """print a progressing counter without spamming the screen"""
    def __init__(self,
                 header="Counter",
                 start=1,
                 end=100,
                 step=1,
                 pipe=sys.stdout,
                 isEnabled=True):
        self.isEnabled = isEnabled
        self.header = header
        self.start = start
        self.cursor = start
        self.end = end
        self.step = step
        self.pipe = pipe
        self.mystring = "{}:".format(self.header) + "[{} / {}] ({}%)"
        self.color = "yellow"

    def setColor(self, color):
        """set the counter color foreground with termcolor.colored"""
        self.color = color

    def toggle(self):
        """toggle counter activity in case we don't want to print
        http://stackoverflow.com/questions/14636350/toggling-decorators
        http://thecodeship.com/patterns/guide-to-python-function-decorators/"""
        self.isEnabled = not self.isEnabled

    def status(self):
        """returns status of the counter"""
        return self.isEnabled

    def next(self):
        """print the next step of the counter"""
        if not self.status():
            return 0
        assert self.cursor <= self.end
        str_end = str(self.end)
        str_cursor = str(self.cursor)
        l = len(str(self.end))
        str_cursor = str_cursor.zfill(l)
        percentage = round(float(self.cursor)/self.end * 100, 2)
        n = "\r"
        n += "\n" if self.cursor == self.start else ""
        self.pipe.write(colored(n+self.mystring.format(str_cursor,
                                                     str_end,
                                                     percentage), self.color))
        self.pipe.flush()
        self.cursor += self.step

    def finish(self):
        if not self.status():
            return 0
        self.pipe.write("\n")
        self.pipe.flush()
        return 0






def do():
    end = 500
    c = Counter(header="QIM", end=end)
    # c.toggle()
    s = 0
    for i in xrange(end):
        s += i
        c.next()
        sleep(0.01)
    print s

def main():
    do()

if __name__ == '__main__':
    sys.exit(main())


