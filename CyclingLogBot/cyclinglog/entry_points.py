#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
CyclingLog entry points module

Copyright (c) 2017 Jorge Luis Rodriguez <jorgeluisrmx@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import unicode_literals

from argparse import ArgumentParser

from cyclinglog.controllers.clog import CyclingLog


def main():
    # creating the parser
    parser = ArgumentParser(description='CyclingLog app manager')
    # adding arguments
    parser.add_argument('-u', '--user', help="username to launch the bot", type=str)
    parser.add_argument('--url', help="user data directory url", type=str)
    parser.add_argument('--update', help="updated user data directory url", type=str)
    parser.add_argument('--delete', help="username to be deleted", type=str)
    parser.add_argument('--users', help="list of users", action='store_true')

    # parsing arguments
    args = parser.parse_args()

    # using arguments
    if args.user and args.url:
        # add new user
        try:
            CyclingLog.create_new_user(args.user, args.url)
        except Exception as e:
            print '    {}'.format(e)
    elif args.user and args.update:
        # update user dir
        try:
            CyclingLog.update_user_dir(args.user, args.update)
        except Exception as e:
            print '    {}'.format(e)
    elif args.delete:
        # delete username
        try:
            CyclingLog.delete_user(args.delete)
        except Exception as e:
            print '    {}'.format(e)
    elif args.user:
        # launching bot for username
        try:
            cl = CyclingLog(username=args.user)
        except Exception as e:
            print '    {}'.format(e)
    elif args.users:
        # print users list
        print CyclingLog.user_list()
    else:
        # is there are users registered launch bot for the first of them
        users = CyclingLog.user_list()
        if users:
            print "Launching CyclingLog Bot for {}".format(users[0])
            cl = CyclingLog(username=users[0])
        else:
            print 'Sorry, no users has been registered'

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~


if __name__ == '__main__':
    main()
