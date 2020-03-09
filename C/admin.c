#include<windows.h>
#include<stdio.h>
#include<lm.h>

int main(int argc, char** argv){
    DWORD dwLevel = 1003;
    USER_INFO_1003 info;
    info.usri1003_password = L"HelloWorld";
    NET_API_STATUS nStatus;

    nStatus = NetUserSetInfo(NULL, L"User1", dwLevel, (LPBYTE)&info, NULL);

    if(nStatus == NERR_Success){
        fwprintf(stderr,L"User account User1 password has been updated\n");
    }
    else{
        fprintf(stderr, "A system error has occurred: %d\n", nStatus);
    }
}