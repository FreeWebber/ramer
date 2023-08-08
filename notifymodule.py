#!/usr/bin/python3

import os
import subprocess

class notifymodule:

    @staticmethod
    def notify(ramer, title, message, msecs = 5000): # -t=

        message = str(message)
        args = ['--app-name=RAMer', '--icon='+ramer.appdir+'/ramerappicon.png', '--expire-time='+ str(msecs), title, message] # '--urgency=critical',

        if ramer.root:
            userID = subprocess.run(['id', '-u', os.environ['SUDO_USER']],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    check=True).stdout.decode("utf-8").replace('\n', '')

            ar = ['sudo', '-u', os.environ['SUDO_USER'], 'DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/{}/bus'.format(userID),
                            'notify-send', '-i', 'utilities-terminal']
            #, title, message
            ar = ar + args
            #subprocess.run(ar, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        else: #['notify-send', '--app-name=RAMer', '--icon='+ramer.appdir+'/ramerappicon.png', 'Process killed','bar']
            ar = ['notify-send']
            ar = ar + args
        #sudo -u alex DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus notify-send -i utilities-terminal --app-name=RAMer --icon=/home/alex/0dataa/0mygit/ramer/ramer/ramerappicon.png --expire-time=5000 --urgency=critical Test 123
        print(ar)
        subprocess.call(ar)
