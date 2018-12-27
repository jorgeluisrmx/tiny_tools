#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
Runs a tow question loon (initial and final date and calc its difference in days.
Enter no answer to exit loop
"""


from __future__ import unicode_literals
from datetime import datetime
import urwid


class DateDif(object):
    def __init__(self):
        self.first = True
        self.initial = None
        self.final = None

    def request(self):
        if self.first:
            return urwid.Pile([urwid.Edit(('I say', "Initial date?\n"))])
        else:
            return urwid.Pile([urwid.Edit(('I say', "Final date?\n"))])


    def set_date(self, date_str):
        try:
            date_ = datetime.strptime(date_str, '%d/%m/%y')
            if self.first:
                self.initial = date_
            else:
                self.final = date_
            self.first = not self.first
        except:
            pass

    def completed(self):
        return True if self.initial and self.final else False

    def result(self, name):
        res = self._calc_date_diff()
        self.initial, self.final = '', ''
        return urwid.Text(('I say', res))

    def _calc_date_diff(self):
        result = (self.final - self.initial).days
        return '\n   = {} DAYS\n\n'.format(result)

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~


class ConversationListBox(urwid.ListBox):
    def __init__(self):
        self.calc = DateDif()
        body = urwid.SimpleFocusListWalker([self.calc.request()])
        super(ConversationListBox, self).__init__(body)

    def keypress(self, size, key):
        key = super(ConversationListBox, self).keypress(size, key)
        if key != 'enter':
            return key
        name = self.focus[0].edit_text
        if not name:
            raise urwid.ExitMainLoop()
        self.calc.set_date(name)
        # add date difference
        if self.calc.completed():
            self.focus.contents[1:] = [(self.calc.result(name), self.focus.options())]
        pos = self.focus_position
        # add date request
        self.body.insert(pos + 1, self.calc.request())
        self.focus_position = pos + 1

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~


def main():
    palette = [('I say', 'default,bold', 'default'), ]
    loop = urwid.MainLoop(ConversationListBox(), palette)
    loop.run()

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~


if __name__ == '__main__':
    main()
