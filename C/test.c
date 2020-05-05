#include<stdio.h>

#include "Crypto.h"

// Compile using gcc test.c -o test.exe -s

int main(){
    // unsigned char data[] = "1234567890123456";
    unsigned char data[] = {0x00,0x11,0x22,0x33,
                            0x44,0x55,0x66,0x77,
                            0x88,0x99,0xaa,0xbb,
                            0xcc,0xdd,0xee,0xff,
                            0xaa};
    // unsigned char key[16] = {0x54,0x45,0x41,0x4D
    //                         ,0x53,0x43,0x4F,0x52
    //                         ,0x50,0x49,0x41,0x4E
    //                         ,0x31,0x32,0x33,0x34};
    unsigned char key[16] = {0x00,0x01,0x02,0x03,
                            0x04,0x05,0x06,0x07,
                            0x08,0x09,0x0a,0x0b,
                            0x0c,0x0d,0x0e,0x0f};
    int data_len = sizeof(data);
    printf("[DEBUG] data:%s\n[DEBUG] length:%d\n",data,data_len);
    EncryptAES(data,key,data_len);
    unsigned char *cipher = data;
    DecryptAES(cipher,key,32);
    
}