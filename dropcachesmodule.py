#!/usr/bin/python3

import os

class dropcachesmodule:

    @staticmethod
    def drop_caches():
        print("sync && echo 1 > /proc/sys/vm/drop_caches && sync && echo 2 > /proc/sys/vm/drop_caches && sync && echo 3 > /proc/sys/vm/drop_caches")
        os.system('sync && echo 1 > /proc/sys/vm/drop_caches && sync && echo 2 > /proc/sys/vm/drop_caches && sync && echo 3 > /proc/sys/vm/drop_caches')
        print("Dropped!")
