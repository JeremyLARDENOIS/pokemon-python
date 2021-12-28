#!/usr/bin/env python3
# coding:utf-8

from lib.game import game
from lib.network import send_msg, recv_msg
import socket
host = ""
port = 3333


##################################MAIN#############################################
socket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)   # Connection type
# Establishment of the server connection
socket.bind((host, port))
print("Launching server")
# Number of attempts allowed
socket.listen(3)

try:
    while True:                                                 # The server doesn't close at the end of the game
        id_player = 1

        # Clients connection
        conn1, addr1 = socket.accept()                          # Waiting for clients
        print(conn1)
        print("Connection", id_player, "accepted")

        send_msg(conn1, id_player)
        msg = recv_msg(conn1)
        if (msg == "OK"):
            print(id_player, "connected players")
            print(addr1)
            id_player += 1
        else:
            print("Connection failed")
            print("Exiting...")
            exit(1)  # Stop server

        # Second client
        conn2, addr2 = socket.accept()
        print("Connection", id_player, "accepted")

        send_msg(conn2, id_player)
        msg = recv_msg(conn2)
        if (msg == "OK"):
            print(id_player, "connected players")
            print(addr2)
            id_player += 1
        else:
            print("connection failed")
            print("Exiting...")
            exit(1)  # Stop server

        send_msg(conn1, "READY")
        send_msg(conn2, "READY")

        msg1 = recv_msg(conn1)
        msg2 = recv_msg(conn2)
        if ((msg1 == "READY") and (msg2 == "READY")):
            print("CONNECTION SUCCESSFULL")

        ###################################
        game(conn1, conn2)  # Launch the game
        ###################################

        # Déconnexion
        send_msg(conn1, "STOP")
        send_msg(conn2, "STOP")
        conn1.close()
        conn2.close()

finally:
    socket.close()
