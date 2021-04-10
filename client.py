#!/usr/bin/env python3

import socket

host = ""
port = 3333

######################################

def send_msg (msg):
    """
    Send a message to server
    Argument: msg
    """
    data = msg.encode("utf-8")
    socket.sendall(data)

def recv_msg ():
    """
    Receive a message from server
    Return: msg
    """
    data = socket.recv(255)
    msg = data.decode("utf-8") 
    return msg

##########################################################

socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try :
    socket.connect((host,port))             # Connecting to serveur
    print("Client connected to server") 
    print("Ask id_player to server...")
    id_player = recv_msg()                  # Receive id
    if (id_player != ""):
        send_msg("OK")                      # Send "OK" for id
        print("Connected with id_player ", id_player)
    else:
        print ("Disconnected")
        exit(1)
    if (recv_msg() == "READY"):             # If server is ready
            send_msg("READY")               # We answer "READY"
    else:
        print("Disconnected from server")
        socket.close()
        exit(2)

### Communication
    status = recv_msg()             # We receive a status from server
    while ((status != "" )and( status != "STOP")): 
        if (status == "READ"):      # If he wants to print something
            send_msg("OK")          # We answer "OK"
            msg = recv_msg()        # He send the message
            print(msg)              # We print it
            if (msg != ""):         # And if it was ok
                status = "OK"       # We answer "OK"
        if (status == "WRITE"):     # If we wants some information
            msg = input('-> ')      # User enter a message
            send_msg(msg)           # And we send it
            #status = recv_msg()    
        if (status == "OK"):        # If we receive "OK"
            send_msg("OK")          # We answer "OK"
        if (status == "WRITE2"):    # Write v2 : allow to send message in same time that other user
            msg = input('-> ')      # User enter a message
            send_msg("OK")          # We say that we are ok for sending
        if (status == "SEND"):      # If he wants the message,
            send_msg(msg)           # We send it

        status = recv_msg()

finally:       
    socket.close()                  # Close the socket
