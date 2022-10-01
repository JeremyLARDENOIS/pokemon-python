#!/usr/bin/env python3
# coding:utf-8

'''Server for the game'''

import socket
import argparse
import sys
from typing import Tuple

from lib.game import game
from lib.network import send_msg, recv_msg
from lib.user import User

argparser: argparse.ArgumentParser = argparse.ArgumentParser()
argparser.add_argument(
    "-H",
    "--host",
    help="host of the server, default is localhost",
    default="0.0.0.0")
argparser.add_argument(
    "-p",
    "--port",
    help="port to listen",
    type=int,
    default=3333)
argparser.add_argument(
    "-v",
    "--verbose",
    help="increase output verbosity",
    action="store_true")
args = argparser.parse_args()

host: str = args.host
port: int = args.port
verbose = args.verbose


class Server:
    """Class that handle the network server for the game"""

    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(5)
        self.users: list[User] = []

    def listen(self) -> User:
        """
        Accept one connection from client
        """
        conn, addr = self.socket.accept()
        print(f"Client connected from {addr}")
        user: User = User("", conn, addr, len(self.users)+1)
        self.users.append(user)

        # Useless but necessary
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
        return user

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

    def game(self, users: Tuple[User, User]) -> None:
        """
        Start a game
        """
        game(users)


##################################MAIN#############################################
if __name__ == "__main__":
    try:
        server: Server = Server()
        print(f"Server is running on {host}:{port}")
        while True:
            user1 = server.listen()
            user2 = server.listen()
            if verbose:
                print("Sending game...")
            ###
            # Put this part in a thread
            server.game((user1, user2))
            user1.stop()
            user2.stop()
            ###
    except KeyboardInterrupt:
        print("\nStopping server...")
        server.stop()
        print("Server stopped")
        sys.exit(0)
    except OSError:
        print("Address already in use")
        sys.exit(1)
