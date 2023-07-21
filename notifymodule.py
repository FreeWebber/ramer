#!/usr/bin/python3

import os
import subprocess

class notifymodule:

    @staticmethod
    def notify(ramer, title, message, msecs = 6000):

        args = ['--app-name=RAMer', '--icon='+ramer.appdir+'/ramerappicon.png', '--expire-time='+ str(msecs), '--urgency=critical', title, message]

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

        subprocess.call(ar)
