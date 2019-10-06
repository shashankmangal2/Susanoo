#include<stdio.h>
#include<iostream>
#include<string.h>
#include<winsock2.h>
#include<windows.h>
#include<ws2tcpip.h>
using namespace std;

#pragma comment(lib, "Ws232.lib")


int Server(int port){

    while(true){

        cout<<"[+] Starting Socket"<<endl;
        SOCKET mySock;
        sockaddr_in saddr;
        WSADATA version;
        WSAStartup(MAKEWORD(2,2), &version);
        
        // Initialising Socket info
        mySock = WSASocket(AF_INET,SOCK_STREAM,IPPROTO_TCP,NULL,(unsigned int)NULL,(unsigned int)NULL);
        // Initialising saddr
        saddr.sin_family = AF_INET;

        saddr.sin_addr.s_addr = INADDR_ANY;
        saddr.sin_port = htons(port);
        
        cout<<"[+] Initialsation of Socket complete"<<endl;
        cout<<"[+] Binding to the port "<<port<<endl;

        int tryPort = bind(mySock,(SOCKADDR*)&saddr,sizeof(saddr));
        if(tryPort < 0){
            cout<<"[-] Failed to bind to port"<<endl;
            closesocket(mySock);
            WSACleanup();
            exit(0);
            // continue;
        }
        else{
            cout<<"[+] Binding Successfull"<<endl;

            cout<<"[+] Starting Listener to port"<<endl;
            int tryListen = listen(mySock,SOMAXCONN); // Potential Problem
            if(tryListen < 0){
                cout<<"[-] Listening Failed"<<endl;
                closesocket(mySock);
                WSACleanup();
                exit(0);
                // continue;
            }
            
            else{
                int len_saddr = sizeof(saddr);
                cout<<"[+] Listening to port "<<port<<endl;
                int tryAccept = accept(mySock,(SOCKADDR*)&saddr, &len_saddr );

                if (tryAccept < 0){
                    cout<<"[-] Accepting connetion Failed"<<endl;
                    closesocket(mySock);
                    WSACleanup();
                    exit(0);
                    // continue;
                }
                else{
                    cout<<"[+] Connection Extablished"<<endl;
                    char SendData[1024] = "Hello from Server";
                    char RecvData[1024];
                    int RecvDataLen = strlen(RecvData)+1;
                    int sendLen = strlen(SendData)+1;
                    send(mySock,SendData,sendLen,0);
                    recv(mySock,RecvData,RecvDataLen,0);
                    cout<<"receved data is:"<<RecvData[0];
                    if((RecvData[0] == 'b' || RecvData[0] == 'B' )&& RecvData[1] == 'y' && RecvData[2] == 'e'){
                        printf("[+] Exit signal Recieved\n");
                        closesocket(mySock);
                        WSACleanup();
                        exit(0);
                    }
                }
            }
        }
    }
    return 0;
}


int main(int argc, char** argv){
    Server(9000);
    return 0;
}