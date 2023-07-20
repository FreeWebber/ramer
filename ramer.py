#!/usr/bin/python3

# python3 -m pip install --upgrade pip
# sudo pip install yachalk
# sudo pip install print-position
'''
RAMer - frees RAM memory if case of lack of by killing processes (OOM killer)
Copyright (C) 2023 Alexandr Nevidlovskyi

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import argparse
from yachalk import chalk
from os import scandir
import os
import signal
import sys
import time
from printPosition.printPosition import printPosition as printp

from pulseaudiomodule import PAmodule
from processesmodule import processesmodule

if __name__ == "__main__":

    debug = 0
    sleep_secs = 10
    limit = 500
    kill = 1
    sound = 1
    priority = ['discord', '/code/code', 'brave/brave', 'brave-beta', 'sublime_text']

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

    showlog = args.showlog
    if args.sound != None: sound = args.sound

    if args.licenese:
        f = open(os.path.dirname(os.path.abspath(__file__)) +'/COPYING.txt',"r")
        lines = f.readlines()
        for line in lines:
            print(line, end='')
        print()
        sys.exit()

    if args.processes:
        processesmodule.init()
        sys.exit()

    #sys.exit()
    if args.intval: sleep_secs = args.intval #if sound: os.system("play notification.mp3 > /dev/null 2>&1") sys.exit()
    if args.limit and args.limit > 100: limit = args.limit
    if args.priority:
        priority = args.priority
        priority = priority.split(',') #print(priority)
    if args.kill != None: kill = args.kill
    #print(args.kill) print(kill)

    #sys.exit()

    PAmodule.init()

    while True:

        f = open("/proc/meminfo","r")
        lines = f.readlines()
        #print(lines[1])
        kb = lines[1].split(' ')
        mb = int(int(kb[-2])/1024) # print(mb) sys.exit()
        #mb = 500
        if showlog: printp('RAM left: '+ str(mb) +' Mb')

        #os.system("sudo -u alex ls /home/alex/0Mega/0/")
        #os.system("ls /home/alex/0Mega/0/")
        #os.system("sudo -u -l alex play /home/alex/0dataa/notification.mp3")
        # subprocess.run(['play', '/home/alex/0dataa/notification.mp3'])

        if debug == 0:
            if(mb < 1000):
                printp(chalk.yellow(mb))
                if 'SUDO_UID' in os.environ: #print(os.environ)
                    print("sync && echo 1 > /proc/sys/vm/drop_caches && sync && echo 2 > /proc/sys/vm/drop_caches && sync && echo 3 > /proc/sys/vm/drop_caches")
                    os.system('sync && echo 1 > /proc/sys/vm/drop_caches && sync && echo 2 > /proc/sys/vm/drop_caches && sync && echo 3 > /proc/sys/vm/drop_caches')
                    #os.system('sync && sudo sh -c "echo 1 > /proc/sys/vm/drop_caches" && sync && sudo sh -c "echo 2 > /proc/sys/vm/drop_caches" && sync && sudo sh -c "echo 3 > /proc/sys/vm/drop_caches"')

        if debug == 0:
            if(mb > limit):
                time.sleep(sleep_secs)
                continue

        printp(chalk.red(mb))
        pids = {}
        sp = "/proc"

        killed = 0
        for entry in scandir(sp):
            if not os.path.isdir(entry):
                continue
            exep = os.path.join(sp, entry.name) +'/exe'
            if not os.path.exists(exep):
                continue

            exerp = os.path.realpath(exep)
            #print(exerp)
            for pname in priority:
                if pname in exerp:
                    pid = exep.split('/')
                    if pname in pids.keys(): #if pids['brave'] == None:
                        continue
                    else:
                        pids[pname] = int(pid[2]) #= []
                    #pids['brave'].append(pid[2])
                    #print(exep)
                    #print(os.path.realpath(exep))
                    #print(entry.name)
                    #continue
            #if os.path.islink(exep) and os.path.exists(exep): #print("Broken: {} -> {}".format(f, )) #print("Broken: {} -> {}".format(f, os.path.realpath(f)))
        printp(pids)
        #sys.exit()

        for pname in priority:
            if killed:
                continue
            if pname in pids.keys():
                killed = 1
                if kill: os.kill(pids[pname], signal.SIGTERM) #or signal.SIGKILL
                printp('Killed: '+ pname)
                if sound: os.system("play notification.mp3 > /dev/null 2>&1")

        time.sleep(sleep_secs)