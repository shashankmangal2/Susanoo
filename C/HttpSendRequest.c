
#include<stdio.h>
#include<windows.h>
#include<wininet.h>
#include<strsafe.h>

// internetopen
// internetconnect
// internetopenrequest

// Compile : gcc .\HttpSendRequest.c -o .\HttpSendRequest.exe -lws2_32 -luser32 -lwininet -s


int connectSendData(char *ip,int port){
    HINTERNET hInternet = InternetOpenA("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",INTERNET_OPEN_TYPE_PRECONFIG,NULL,NULL,0);
    // Sets User-Agent in request

    if(hInternet == NULL){
        printf("[DEBUG] Error while InternetOpen\n");
        return 0;
    }

    HINTERNET hConnect = InternetConnectA(hInternet,ip,port,NULL,NULL,INTERNET_SERVICE_HTTP,0,0);
    if(hConnect == NULL){
        printf("[DEBUG] Error while InternetConnect\n");
        return 0;
    }

    PCTSTR parAcceptTypes[] = {"text/*", NULL};
    // Sending a Get request for the index.html page 
    // To send HTTPS request 
    // HINTERNET hRequest = HttpOpenRequestA(hConnect,"GET","index.html", NULL, NULL, parAcceptTypes, INTERNET_FLAG_SECURE,0 );
    // To send normal HTTP request 
    HINTERNET hRequest = HttpOpenRequestA(hConnect,"GET","index.html", NULL, NULL, parAcceptTypes, 0,0 );


    if(hRequest == NULL){
        printf("[DEBUG] Error while InternetOpenRequest\n");
        return 0;
    }

    BOOL bRequestSent = HttpSendRequestA(hRequest,NULL,0,NULL,0);    // Make changes here to send some cookies and other POST data
    if(bRequestSent == 0){
        printf("[DEBUG] Error while HttpSendRequest\n");
        return 0;
    }

    char buffer[1024];
    char RecvBuff[20000];
    memset(buffer, 0, sizeof(buffer));      // Clearing Out the memory
    memset(RecvBuff, 0, sizeof(RecvBuff));  // Clearing Out the memory

    BOOL bKeepReading = 1;
    DWORD dwBytesRead = -1;
    printf("[DEBUG] Reading is starting\n");
    // Reading the buffer here  
    while(bKeepReading && dwBytesRead != 0){
        bKeepReading = InternetReadFile(hRequest, buffer, 1024, &dwBytesRead);
        StringCchCatA(RecvBuff, 20000, buffer);
        memset(buffer, 0, sizeof(buffer));
    }
    printf("[DEBUG] Reading Done\n");
    printf("%s",RecvBuff);              // Printing buffer recieved
    return 0;

}

int main(int argc, char** argv){
    char *address = argv[1];
    int port = atoi(argv[2]);
    connectSendData(address,port);
    // connectSendData("iczn.org",80);
}