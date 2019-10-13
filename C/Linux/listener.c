#include<stdio.h>
#include<string.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<stdlib.h>
#include<netinet/in.h>
#include<arpa/inet.h>
#include<time.h>

void error(char *msg){
    perror(msg);
    exit(1);
}

int main(int argc, char **argv){
    if (argc < 2){
        fprintf(stderr, "Port no provided, Program terminalted\n");
        exit(1);
    }

    int sockfd, newsockfd, portno, n;
    char buffer[1024];

    struct sockaddr_in server_addr, client_addr;
    socklen_t clilen;

    sockfd = socket(AF_INET,SOCK_STREAM,0);
    if(sockfd < 0){
        close(sockfd);
        error("Error setting up socket");
    }

    bzero((char *) &server_addr , sizeof(server_addr));
    portno = atoi(argv[1]);

    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(portno);

    if(bind(sockfd, (struct  sockaddr *) &server_addr,sizeof(server_addr)) < 0 ){
        close(sockfd);
        error("Error while binding to port");
    }

    printf("Listening to port %s\n",argv[1]);
    listen(sockfd, 10); 
    clilen = sizeof(client_addr);
    
    newsockfd = accept(sockfd,(struct sockaddr *) &client_addr, &clilen);

    if(newsockfd < 0){
        printf("Error Code:%d\n",newsockfd);
        close(newsockfd);
        close(sockfd);
        error("Error while accepting socket");
    }
    else{
        time_t T = time(NULL);
        struct tm tm = *localtime(&T);
        char filename[40];
        snprintf(filename,40,"/root/connection-%d.log",portno);

        FILE *fptr;
        fptr = fopen(filename,"a");
        char ip[20];
        inet_ntop(AF_INET,&client_addr.sin_addr,ip,20);
        printf("Connected to ncat listner on %d/%d/%d at %d:%d:%d from %s\n",tm.tm_mday,tm.tm_mon+1,tm.tm_year+1900,tm.tm_hour,tm.tm_min,tm.tm_sec,ip);
        fprintf(fptr,"Connected to ncat listner on %d/%d/%d at %d:%d:%d from %s\n",tm.tm_mday,tm.tm_mon+1,tm.tm_year+1900,tm.tm_hour,tm.tm_min,tm.tm_sec,ip);
    }
    close(newsockfd);
    close(sockfd);
    return 0;
}