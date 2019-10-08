#include<iostream>
#include<string.h>
#include<winsock2.h>
#include<windows.h>
#include<ws2tcpip.h>
using namespace std;

#pragma comment(lib, "Ws2_32.lib")s


int Server(int port){

    char buffer[1024];
    // bzero(buffer,1024);
    cout<<"[+] Starting Socket"<<endl;
    SOCKET mySock;
    sockaddr_in saddr;
    WSADATA version;
    WSAStartup(MAKEWORD(2,2), &version);
    mySock = WSASocket(AF_INET,SOCK_STREAM,IPPROTO_TCP,NULL,(unsigned int)NULL,(unsigned int)NULL);
    saddr.sin_family = AF_INET;

    saddr.sin_addr.s_addr = INADDR_ANY;
    saddr.sin_port = htons(port);

    cout<<"[+] Binding to the port "<<port<<endl;
    // Trying to bind to the port
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
        
        // Turning on the listener
        cout<<"[+] Starting Listener to port "<<endl;
        int listenTry = listen(mySock,SOMAXCONN);
        if(listenTry < 0){
            cout<<"[-] Listening Failed"<<endl;
            closesocket(mySock);
            WSACleanup();
            exit(0);
            // continue;
        }
        
        else{
            cout<<"[+] Listening to port "<<port<<endl;
            int sizeSaddr = sizeof(saddr);
            SOCKET AcceptSock = accept(mySock,(SOCKADDR*)&saddr,(socklen_t*)&sizeSaddr);
            if(AcceptSock == INVALID_SOCKET){
                cout<<"[-] Accepting connection Failed"<<endl;
                closesocket(mySock);
                WSACleanup();
                exit(0);
                // continue;
            }
            else{
                closesocket(mySock);
                cout<<"[+] Connection Established \n Enjoy Your Shell....."<<endl;
                char SendData[1024] = "hello";
                int iSendDataBuffer = strlen(SendData)+1;
                send(AcceptSock,SendData,iSendDataBuffer,0);
                recv(AcceptSock,buffer,strlen(buffer)+1,0);

            }

        }
    }
    return 0;
}

int main(int argc,char** argv){
    if(argc == 2){
        int port = atoi(argv[1]);
        Server(port);
    }
    else{
        Server(8080);
    }
    return 0;
}