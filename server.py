#!/usr/bin/env python3
# coding:utf-8

from lib.game import game
from lib.network import send_msg, recv_msg
from lib.user import User
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
        # Clients connection
        conn, addr = socket.accept()
        user1 = User("", conn, addr, 1)
        print(user1.id, "connected")

        send_msg(user1.conn, user1.id)
        msg = recv_msg(user1.conn)
        if (msg == "OK"):
            print("1 connected player")
            print(user1.addr)
        else:
            print("Connection failed")
            print("Exiting...")
            exit(1)  # Stop server

        # Second client
        conn, addr = socket.accept()
        user2 = User("", conn, addr, 2)
        print(user2.id, "connected")

        send_msg(user2.conn, user2.id)
        msg = recv_msg(user2.conn)
        if (msg == "OK"):
            print("2 connected players")
            print(user2.addr)
        else:
            print("connection failed")
            print("Exiting...")
            exit(1)  # Stop server

        send_msg(user1.conn, "READY")
        send_msg(user2.conn, "READY")

        msg1 = recv_msg(user1.conn)
        msg2 = recv_msg(user2.conn)
        if ((msg1 == "READY") and (msg2 == "READY")):
            print("CONNECTION SUCCESSFULL")

        ###################################
        game(user1, user2)  # Launch the game
        ###################################

        # Déconnexion
        send_msg(user1.conn, "STOP")
        send_msg(user2.conn, "STOP")
        user1.conn.close()
        user2.conn.close()

finally:
    socket.close()
