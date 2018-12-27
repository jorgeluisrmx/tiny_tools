#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
Renames svg, jpg, and png files, removing the ID-number at the end of the filename
"""

from __future__ import print_function
import os

def new_name(name):
    base_name, extension = os.path.splitext(name)
    parts = base_name.split('_')
    if parts[-1].isdigit():
        return True, '_'.join(parts[:-1]) + extension
    return False, name

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~


def main():
    # base counter
    fr = 0
    # listing directory content
    for name in os.listdir('.'):
        name_fpath = os.path.abspath(name)
        # avoid dirs and fiter by extension
        if os.path.isfile(name) and os.path.splitext(name)[-1] in ['.jpg', '.png', '.svg']:
            res, newn = new_name(name)
            if res:
                os.rename(name, newn)
                fr += 1
    print("    {} files renamed".format(fr))

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~


if __name__ == '__main__':
    main()

