#include<stdio.h>
//#include<string.h>
#include<winsock2.h>
#include<windows.h>
#include<ws2tcpip.h>


int Server(int port){

    while(1){

        printf("[+] Starting Socket\n");
        SOCKET mySock;
        struct sockaddr_in saddr;
        WSADATA version;
        WSAStartup(MAKEWORD(2,2), &version);
        
        // Initialising Socket info
        mySock = WSASocket(AF_INET,SOCK_STREAM,IPPROTO_TCP,NULL,0,WSA_FLAG_OVERLAPPED);
        // Initialising saddr
        saddr.sin_family = AF_INET;

        saddr.sin_addr.s_addr = INADDR_ANY;
        saddr.sin_port = htons(port);
        
        printf("[+] Initialsation of Socket complete\n");
        printf("[+] Binding to the port %d\n",port);

        int tryPort = bind(mySock,(SOCKADDR*)&saddr,sizeof(saddr));
        if(tryPort < 0){
            printf("[-] Failed to bind to port\n");
            closesocket(mySock);
            WSACleanup();
            exit(0);
            // continue;
        }
        else{
            printf("[+] Binding Successfull\n");

            printf("[+] Starting Listener to port\n");
            int tryListen = listen(mySock,SOMAXCONN); // Potential Problem
            if(tryListen < 0){
                printf("[-] Listening Failed\n");
                closesocket(mySock);
                WSACleanup();
                exit(0);
                // continue;
            }
            
            else{
                int len_saddr = sizeof(saddr);
                printf("[+] Listening to port %d\n",port);
                int tryAccept = accept(mySock,(SOCKADDR*)&saddr, &len_saddr );

                if (tryAccept < 0){
                    printf("[-] Accepting connetion Failed\n");
                    closesocket(mySock);
                    WSACleanup();
                    exit(0);
                    // continue;
                }
                else{
                    printf("[+] Connection Extablished\n");
                    char SendData[1024] = "Hello from Server";
                    char RecvData[1024];
                    int RecvDataLen = sizeof(RecvData)+1;
                    int sendLen = sizeof(SendData)+1;
                    send(mySock,SendData,sendLen,0);
                    recv(mySock,RecvData,RecvDataLen,0);
                    printf("receved data is: %s\n",RecvData[0]);
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
