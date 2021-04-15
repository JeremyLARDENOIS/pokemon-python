#!/usr/bin/env python3

import socket

host = ""
port = 3333

from lib.network import *

socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try :
    socket.connect((host,port))             # Connecting to serveur
    print("Client connected to server") 
    print("Ask id_player to server...")
    id_player = recv_msg(socket)                  # Receive id
    if (id_player != ""):
        send_msg(socket,"OK")                      # Send "OK" for id
        print("Connected with id_player ", id_player)
    else:
        print ("Disconnected")
        exit(1)
    if (recv_msg(socket) == "READY"):             # If server is ready
            send_msg(socket,"READY")               # We answer "READY"
    else:
        print("Disconnected from server")
        socket.close()
        exit(2)

### Communication
    status = recv_msg(socket)             # We receive a status from server
    while ((status != "" )and( status != "STOP")): 
        if (status == "READ"):      # If he wants to print something
            send_msg(socket,"OK")          # We answer "OK"
            msg = recv_msg(socket)        # He send the message
            print(msg)              # We print it
            if (msg != ""):         # And if it was ok
                status = "OK"       # We answer "OK"
        if (status == "WRITE"):     # If we wants some information
            msg = input('-> ')      # User enter a message
            send_msg(socket,msg)           # And we send it
            #status = recv_msg()    
        if (status == "OK"):        # If we receive "OK"
            send_msg(socket,"OK")          # We answer "OK"
        if (status == "WRITE2"):    # Write v2 : allow to send message in same time that other user
            msg = input('-> ')      # User enter a message
            send_msg(socket,"OK")          # We say that we are ok for sending
        if (status == "SEND"):      # If he wants the message,
            send_msg(socket,msg)           # We send it

        status = recv_msg(socket)

finally:       
    socket.close()                  # Close the socket
