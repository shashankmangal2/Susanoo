#!/usr/bin/python

import multiprocessing
import os
import sys
import time
import logging

def targetfunc(i):
    while(True):
        name = multiprocessing.current_process().name
        print("[!] "+str(name)+" is running")
        time.sleep(2)

if __name__ == '__main__':
    multiprocessing.log_to_stderr()
    logger = multiprocessing.get_logger()
    logger.setLevel(logging.INFO)
    proc_name = ""
    print("[+] Creating some processes\n")
    process_list = []
    for i in range(4):
        proc = multiprocessing.Process(target=targetfunc, args=(proc_name,))
        process_list.append(proc)
        proc_name = proc.name
        proc.start()
    print("\nprocess creation is done\n")
    process_list[2].terminate()
    del process_list[2]
    print("\nprocess 3 is killed\n")
    time.sleep(5)
    print("killing all processes\n")
    print(process_list[2].name)
    for i in range(len(process_list)):
        proc_name = process_list[i].name
        print(proc_name)
        process_list[i].terminate()
    
