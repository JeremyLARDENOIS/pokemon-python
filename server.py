#!/usr/bin/env python3
# coding:utf-8

from lib.game import game
from lib.network import send_msg, recv_msg
from lib.user import User
import socket
host = ""
port = 3333


class Server:
    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(5)
        self.users = []

    def listen(self) -> None:
        """
        Accept connections from clients and create a new thread for each one
        """
        # while True:
        if True:
            conn, addr = self.socket.accept()
            print(f"Client connected from {addr}")
            user = User("", conn, addr, len(self.users))
            self.users.append(user)

            # TO REMOVE
            # Send id to client and wait for "OK"
            send_msg(conn, str(user.id))
            if recv_msg(conn) == "OK":
                print(f"Client {user.id} connected")
                # Send "READY" to client
                send_msg(conn, "READY")
                # Wait for "READY" from client
                if recv_msg(conn) == "READY":
                    pass
                    # user.start()

    def stop(self) -> None:
        """
        Stop the server
        """
        for user in self.users:
            user.stop()
        self.socket.close()

    def unconnect(self, user: User) -> None:
        """
        Unconnect the user
        """
        self.users.remove(user)
        user.stop()

    def game(self):
        """
        Start a game
        """
        game(self.users)


##################################MAIN#############################################
if __name__ == "__main__":
    try:
        server = Server()
        print("Server is running...")
        server.listen()
        server.listen()
        print("Sending game...")
        server.game()
        server.stop()
        print("Server is stopped")
    except KeyboardInterrupt:
        print("\nStopping server...")
        server.stop()
        print("Server stopped")
        exit(0)
    except Exception as e:
        print("Fatal error: ", e)
        server.stop()
        exit(1)
