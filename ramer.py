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

from yachalk import chalk # import dbus
from os import scandir
import os
import signal # import sys
import time
from print_position import print_pos as printp #from printPosition.printPosition import printPosition as printp

from pulseaudiomodule import PAmodule
from notifymodule import notifymodule
from argsmodule import argsmodule
from dropcachesmodule import dropcachesmodule

from timeit import default_timer as timer

class RAMer:

    appdir = os.path.dirname(os.path.abspath(__file__))
    root = 0

    kill = 1
    limit = 500
    showlog = 0
    sleep_secs = 10
    sound = 1
    ft = False

    def __init__(self):
        self.run(self)

    @staticmethod
    def getinfo(self):
        f = open("/proc/meminfo","r")
        lines = f.readlines()
        mb = lines[1].split(' ')
        mb = int(int(mb[-2])/1024) # print(mb) sys.exit() #mb = 500
        if self.showlog: printp('RAM left: '+ str(mb) +' Mb')
        return mb

    @staticmethod
    def run(self):

        count = 0
        drop_caches_count = 0
        debug = 0
        priority = ['discord', '/code/code', 'brave/brave', 'brave-beta', 'sublime_text']

        if 'SUDO_UID' in os.environ: self.root = 1

        argsmodule.init(self) #print(args.kill) print(kill)
        #sys.exit()
        PAmodule.init()

        start = timer() #notifymodule.notify(self, 'Test', 123, 5000)

        mb = self.getinfo(self)
        printp(chalk.red(mb))

        while True:
            printp(count)

            end = timer()
            if(end - start) > 1800:
                start = timer()
                printp('dropcachesmodule.drop_caches() #1')
                dropcachesmodule.drop_caches()

            count = count+1
            if count > 1000: count = 0
            mb = self.getinfo(self)

            if self.ft == False:
                self.ft = True
                printp('dropcachesmodule.drop_caches() #2')
                dropcachesmodule.drop_caches()
                mb = self.getinfo(self)
            printp(self.sleep_secs)
            time.sleep(self.sleep_secs)
            printp(self.sleep_secs)

            #print(count % 2) if count % 30 == 0:
            if debug == 0:
                if(mb < 2000):
                    printp(chalk.yellow(mb))
                    if self.root: #print(os.environ)
                        if drop_caches_count == 0:
                            dropcachesmodule.drop_caches()
                            drop_caches_count+=1
                            continue
                        drop_caches_count+=1
                        print('drop_caches_count: '+ str(drop_caches_count))
                        if drop_caches_count > 5: drop_caches_count = 0

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
            printp(pids) #sys.exit()

            for pname in priority:
                if killed:
                    continue
                if pname in pids.keys():
                    killed = 1
                    if self.kill: os.kill(pids[pname], signal.SIGTERM) #or signal.SIGKILL
                    notifymodule.notify(self, 'Process killed', pname, 5000)
                    printp('Killed: '+ pname)
                    if self.sound: os.system("play notification.mp3 > /dev/null 2>&1")

if __name__ == "__main__":
    ramer = RAMer()