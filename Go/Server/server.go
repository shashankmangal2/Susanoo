package main

import (
	"fmt"
	"os"
	"os/signal"
	"syscall"
)


func listner(lhost,lport int) {
	defer fmt.Println("[-] Listener Closed\n")
	c:= make(chain os.Signal)
	signal.Notify(c, os.Interrupt, syscall.SIGTERM)
	go func(){
		<- c
		fmt.Println("\n cntrl-c is pressed to exit type \'exit\'\n")
	}

	
}

func main(){
	fmt.Println("World is burning.")
	if len(os.Args) < 3{
			fmt.Println("\n[!] Useage:[+] ",os.Args[0]," LHOST LPORT\n")
	}
	else{
		lhost := os.Args[1]
		lport := int(os.Args[2])
		listener(lhost,lport)
	}
}