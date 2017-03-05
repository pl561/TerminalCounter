#! /usr/bin/env python
# -*-coding:utf-8 -*

import sys
import time
import os
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
        self.mystring = "{}:".format(self.header) + "[{} / {}] ({}%)".ljust(10)
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


class Counters(object):
    """displays a line of integer counters with percentage display"""
    def __init__(self, headers, ranges, pipe=sys.stdout):
        self.headers = headers
        self.ranges = []
        self.cursors = []
        for rg in ranges:
            if len(rg) == 2:
                s, e = rg
                self.ranges.append((s, e, 1))
            elif len(rg) == 3:
                self.ranges.append(rg)
            else:
                raise ValueError('Expected tuple (start, end, step)')
            self.cursors.append(rg[0])

        self.pipe = pipe
        self.display_format = "{}:[{} / {}] ({}%)"
        self.color = "yellow"
        self.terminal_cursor = True
        self.toggle_cursor()

    def next(self, counterno):
        """moves forward the counterno-th cursor"""
        nb_counters = len(self.ranges)
        counter_data_iterator = zip(range(nb_counters),
                                    self.headers, self.ranges, self.cursors)
        display_formats = []
        for index, header, bounds, cursor in counter_data_iterator:
            start, end, step = bounds
            str_end = str(end)
            len_fill = len(str_end)
            str_cursor = str(cursor)
            str_cursor = str_cursor.zfill(len_fill)
            percentage = round(float(cursor-start+1)/(end-start+1)*100, 2)
            display_format = self.display_format.format(header,
                                                        str_cursor, str_end,
                                                        percentage)
            display_formats.append(display_format)
            if cursor == end and index != 0:
                self.cursors[index] = start

            if index == counterno:
                self.cursors[index] += step

        self.pipe.write(colored(", ".join(display_formats)+'\r', self.color))
        self.pipe.flush()


    def toggle_cursor(self):
        """displays or hides the terminal cursor"""
        if self.terminal_cursor:
            os.system('setterm -cursor off')
        else:
            os.system('setterm -cursor on')
        # toggle
        self.terminal_cursor = not self.terminal_cursor


    def finish(self):
        self.pipe.write("\n")
        self.pipe.flush()
        self.toggle_cursor()


def test_counter():
    end = 25
    c = Counter(header="Deadline dans (en s)", end=end)
    s = 0
    for i in xrange(end):
        s += i
        c.next()
        time.sleep(60.)
    print s

def test_counters():
    headers = ['hd1', 'hd2', 'hd3']
    ranges = [(1, 10), (10, 20), (30, 40)]

    ctrs = Counters(headers, ranges)

    for i in range(10):
        for j in range(10, 20):
            for k in range(30, 40):
                ctrs.next(2)
                time.sleep(0.01)
            ctrs.next(1)
        ctrs.next(0)
    ctrs.finish()

def do():
    try:
        test_counters()
    finally:
        os.system('setterm -cursor on')

def main():
    do()

if __name__ == '__main__':
    sys.exit(main())


