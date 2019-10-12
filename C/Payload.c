#include<stdio.h>	// printf, scanf
#include<winsock2.h>
#include<Windows.h>
#include<ws2tcpip.h>
#include<strsafe.h>	// StringCchLength, StringCchCopy, StringCchCat 
#pragma comment(lib, "Ws2_32.lib")
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

	// else {
	// 	printf("Nothing Happend: %s", argv[1]);
	// }
	HTTPconnections();

	return 0;
}