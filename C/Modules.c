#include<stdio.h>
#include<windows.h>

void HideWindow(){
    HWND hwnd = GetConsoleWindow();
    if(hwnd == NULL){
        printf("\nGetConosleWindow is NULL");
        sleep(1);
        return;
    }
    printf("\nAbout to close window");
    sleep(1);
    printf("\nclosing window");
    sleep(1);
    ShowWindow(hwnd, SW_MINIMIZE);
    ShowWindow(hwnd, SW_HIDE);
    FILE *fp;
    fp = fopen("C:\\Users\\shash\\Susanoo\\C\\test.txt","a+");
    fprintf(fp,"writing stuff\n");
    fclose(fp);
    sleep(5);
    return;
}
void InstallService(){
    SC_HANDLE schSCManager;
    SC_HANDLE schService;
    TCHAR s
}

int main(int argc, char **argv){
    //hide();

}