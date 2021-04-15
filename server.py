#!/usr/bin/env python3
#coding:utf-8

host = ""
port = 3333

import socket

from lib.network import *
from lib.game import *

##################################MAIN#############################################
socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)   # Type de connexion
socket.bind((host,port))                                    # Establishment of the server connection
print("Launching server") 
socket.listen(3)                                            # Number of attempts allowed

while True:                                                 # The server doesn't close at the end of the game
    id_player = 1

    # Clients connection
    conn1, addr1 = socket.accept()                          # Waiting for clients
    print(conn1)
    print("Connexion", id_player, "accepté")

    send_msg(conn1,id_player)
    msg = recv_msg(conn1)
    if (msg == "OK"):
        print (id_player,"joueur(s) connecté(s)")
        print(addr1)
        id_player += 1
    else:
        print("echec de la connection")
        exit(1) # Stop server
    
    # Second client
    conn2, addr2 = socket.accept()
    print("Connexion", id_player, "accepté")

    send_msg(conn2,id_player)
    msg = recv_msg(conn2)
    if (msg == "OK"):
        print (id_player,"joueur(s) connecté(s)")
        print(addr2)
        id_player += 1
    else:
        print("echec de la connection")
        exit(1) # Stop server

    send_msg(conn1,"READY")
    send_msg(conn2,"READY")

    msg1 = recv_msg(conn1)
    msg2 = recv_msg(conn2)
    if ((msg1 == "READY")and(msg2 == "READY")):
        print("CONNECTION SUCCESSFULL")

    ###################################
    game(conn1,conn2) # Launch the game
    ###################################

    #Déconnexion
    send_msg(conn1,"STOP") 
    send_msg(conn2,"STOP")
    conn1.close() 
    conn2.close() 

socket.close()


