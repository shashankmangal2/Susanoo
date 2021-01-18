package main

import (
	"fmt"
	"os"
	"os/signal"
	"syscall"
	"time"
	"net/http"
	"sync"
)


/**********************************
1. Add handlerFunc for handling All the pages
2. Add index page of Apache
3. Host multiple URL according to requests
4. Parse Body to get data and POST data accordingly
5. Add API based calling
**********************************/

func APIExec(w http.ResponseWriter, req *http.Request){
	api_call := req.Header.Get
}


func API(){
	defer wg.Done()

	var err := nil
	http.HandleFunc("/test",APIExec)
	http.ListenAndServe(":9090",err)
	if(err != nil){
		log.Fatal(err)
	}
}

func listner(lhost string ,lport int) {
	defer fmt.Println("[-] Listener Closed\n")
	wg := new(sync.WaitGroup)
	fmt.Println("[+] Listener Opened\n")
	time.Sleep(10 * time.Second)
	wg.Add(2)
	go API()
	// go handler()
		
}

func main(){
	fmt.Println("World is burning.")
	c := make(chan os.Signal, 1)
    signal.Notify(c, syscall.SIGINT, syscall.SIGTERM)
    go func() {
        <-c
        fmt.Println("\ncntrl-c is pressed to exit type 'exit'\n")	// ASK paranoid how to print this statement again and again when ctrl-c is pressed
        // os.Exit(1)
    }()
	if len(os.Args) < 3{
		fmt.Println("\n[!] Useage:[+] ",os.Args[0]," LHOST LPORT\n")
	} else{
		// lhost := os.Args[1]
		// lport := int(os.Args[2])
		lhost := "127.0.0.1"
		lport := 8080
		listner(lhost,lport)
	}
}