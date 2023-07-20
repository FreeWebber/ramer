#!/usr/bin/python3

import subprocess

class processesmodule:

    @staticmethod
    def init(): #print(PAmodule.get_pids_by_script_name('pulseaudio'))
        #os.system("ps aux | grep brave | awk '{print $11}' | tr -s ' '")
        output = subprocess.check_output('ps aux | awk \'{print $11}\'', shell=True)
        output = output.decode()
        output = output.split('\n')
        #print(output)
        output = list(set(output))

        for proc in output: #print(proc) print(proc.startswith("/"))
            if proc.startswith("/"): print(proc)