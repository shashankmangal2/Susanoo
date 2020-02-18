#!/usr/bin/python3

import multiprocessing
import os
import sys
import time
import logging
import socket
import threading

flag = True

def receiving(client):
    while True:
        if(flag == False):
            client.shutdown(socket.SHUT_RDWR)
            client.close()
            break
        else:
            data = client.recv(4096)
            sys.stdout.write(data.decode())
            
def sending(client):
    RecvThread = threading.Thread(target=receiving, args=(client,))
    RecvThread.start()
    sys.stdout.write("Thread Started \n")
    while True:
        sys.stdout.write("Shell > ")
        command = input()
        if command == "exit":
            flag == False
            break
        else:
            command = command + "\n"
            client.send(command.encode())
            sys.stdout.write("command is sent %s" % (command))
    


if __name__ == '__main__':
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('',8082))
    s.listen(4)
    sys.stdout.write("Listening is on\n")
    (client,client_addr) = s.accept()
    sys.stdout.write("Connection accepted\n")
    time.sleep(0.5)
    # data = client.recv(4096)
    # sys.stdout.write(data)
    sending(client)
    client.close()

# hello = "hello world"

# def hellofunc():
#     global hello
#     print(hello)

# hellofunc()


# def targetfunc(i):
#     while(True):
#         name = multiprocessing.current_process().name
#         print("[!] "+str(name)+" is running")
#         time.sleep(2)

# if __name__ == '__main__':
#     multiprocessing.log_to_stderr()
#     logger = multiprocessing.get_logger()
#     logger.setLevel(logging.INFO)
#     proc_name = ""
#     print("[+] Creating some processes\n")
#     process_list = []
#     for i in range(4):
#         proc = multiprocessing.Process(target=targetfunc, args=(proc_name,))
#         process_list.append(proc)
#         proc_name = proc.name
#         proc.start()
#     print("\nprocess creation is done\n")
#     process_list[2].terminate()
#     del process_list[2]
#     print("\nprocess 3 is killed\n")
#     time.sleep(5)
#     print("killing all processes\n")
#     print(process_list[2].name)
#     for i in range(len(process_list)):
#         proc_name = process_list[i].name
#         print(proc_name)
#         process_list[i].terminate()
    
