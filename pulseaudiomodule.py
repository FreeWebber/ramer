#!/usr/bin/python3

import os
import psutil

class PAmodule:

    @staticmethod
    def init(): #print(PAmodule.get_pids_by_script_name('pulseaudio'))
        pid = PAmodule.get_pid('pulseaudio')
        if pid == None: os.system("pulseaudio") #os.system("pulseaudio -D 3>&1 1>&2 2>&3 1 null")

    @staticmethod
    def get_pid(string):

        rpid = None
        for proc in psutil.process_iter():

            try:
                cmdline = proc.cmdline()
                pid = proc.pid
            except psutil.NoSuchProcess:
                continue

            #print(cmdline)
            if (len(cmdline) >= 2
                and string in cmdline[0]):
                rpid = pid

        return rpid