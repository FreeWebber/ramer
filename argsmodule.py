#!/usr/bin/python3

import argparse

from processesmodule import processesmodule

class argsmodule:

    @staticmethod
    def init(ramer):

        args = argsmodule.parse(ramer)

        ramer.showlog = args.showlog
        if args.sound != None: ramer.sound = args.sound

        if args.licenese:
            f = open(ramer.appdir +'/COPYING.txt',"r")
            lines = f.readlines()
            for line in lines:
                print(line, end='')
            print()
            sys.exit()

        if args.processes:
            processesmodule.init()
            sys.exit()

        #sys.exit()
        if args.intval: ramer.sleep_secs = args.intval #if sound: os.system("play notification.mp3 > /dev/null 2>&1") sys.exit()
        if args.limit and args.limit > 100: ramer.limit = args.limit
        if args.priority:
            priority = args.priority
            ramer.priority = priority.split(',') #print(priority)
        if args.kill != None: ramer.kill = args.kill

        return args

    def parse(ramer):

        parser = argparse.ArgumentParser(description='Example: --showlog 1')

        parser.add_argument('--limit', type=int, nargs='?', help='set limit of minimum free memory since start killing programs, megabytes, default 500, always >100')
        parser.add_argument('--intval', type=int, nargs='?', help='set interval in seconds, default 10')
        parser.add_argument('--sound', type=int, nargs='?', help='1 for play sound on killing process')
        parser.add_argument('--showlog', type=int, nargs='?', help='1 for showing log')
        parser.add_argument('--priority', nargs='?', help='set penultimate part of name of cli proccess that must be killed in case the lack of RAM. The longer string the better for definition. Must be divded by comma, ex: discord,/code/code,brave/brave,brave-beta,sublime_text \
        Default list: `discord,/code/code,brave/brave,brave-beta,sublime_text`')
        parser.add_argument('--processes', type=int, nargs='?', help='for showing names for creating list of processes that must be killed')
        parser.add_argument('--kill', type=int, nargs='?', help='kill process?, default 1')
        parser.add_argument('--licenese', type=int, nargs='?', help='Show licenese')
        args = parser.parse_args()

        return args
