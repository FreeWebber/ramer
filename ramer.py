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
'''
Image of app icon created by Freepik - Flaticon, https://www.flaticon.com/free-icons/ram
'''

import dbus
from yachalk import chalk
from os import scandir
import os
import signal
import sys
import time
from printPosition.printPosition import printPosition as printp

from pulseaudiomodule import PAmodule
from notifymodule import notifymodule
from argsmodule import argsmodule

class RAMer:

    appdir = os.path.dirname(os.path.abspath(__file__))
    root = 0

    kill = 1
    limit = 500
    showlog = 0
    sleep_secs = 10
    sound = 1

    def __init__(self):
        self.run(self)

    @staticmethod
    def run(self):

        drop_caches_count = 0
        debug = 0
        priority = ['discord', '/code/code', 'brave/brave', 'brave-beta', 'sublime_text']

        if 'SUDO_UID' in os.environ: self.root = 1

        argsmodule.init(self)
        #print(args.kill) print(kill)

        #sys.exit()

        PAmodule.init()

        '''if root:
            notify('foo','bar')
        else:
            subprocess.call(['notify-send', '--app-name=RAMer', '--icon='+appdir+'/ramerappicon.png', 'Process killed','bar'])
        '''
        #notifymodule.notify(self, 'Process killed','bar') sys.exit()

        while True:

            f = open("/proc/meminfo","r")
            lines = f.readlines()
            #print(lines[1])
            kb = lines[1].split(' ')
            mb = int(int(kb[-2])/1024) # print(mb) sys.exit()
            #mb = 500
            if self.showlog: printp('RAM left: '+ str(mb) +' Mb')

            #os.system("sudo -u alex ls /home/alex/0Mega/0/")
            #os.system("ls /home/alex/0Mega/0/")
            #os.system("sudo -u -l alex play /home/alex/0dataa/notification.mp3")
            # subprocess.run(['play', '/home/alex/0dataa/notification.mp3'])

            if debug == 0:
                if(mb < 1000):
                    printp(chalk.yellow(mb))
                    if self.root: #print(os.environ)
                        if drop_caches_count == 0:
                            print("sync && echo 1 > /proc/sys/vm/drop_caches && sync && echo 2 > /proc/sys/vm/drop_caches && sync && echo 3 > /proc/sys/vm/drop_caches")
                            os.system('sync && echo 1 > /proc/sys/vm/drop_caches && sync && echo 2 > /proc/sys/vm/drop_caches && sync && echo 3 > /proc/sys/vm/drop_caches')
                        drop_caches_count+=1
                        if drop_caches_count > 10: drop_caches_count = 0
                        #os.system('sync && sudo sh -c "echo 1 > /proc/sys/vm/drop_caches" && sync && sudo sh -c "echo 2 > /proc/sys/vm/drop_caches" && sync && sudo sh -c "echo 3 > /proc/sys/vm/drop_caches"')

            if debug == 0:
                if(mb > self.limit):
                    time.sleep(self.sleep_secs)
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
                    notifymodule.notify(self, 'Process killed', pname)
                    printp('Killed: '+ pname)
                    if sound: os.system("play notification.mp3 > /dev/null 2>&1")

            time.sleep(sleep_secs)

if __name__ == "__main__":
    ramer = RAMer()