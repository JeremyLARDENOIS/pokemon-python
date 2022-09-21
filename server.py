#!/usr/bin/env python3
# coding:utf-8

from lib.game import game
from lib.network import send_msg, recv_msg
from lib.user import User
import socket
import argparse

argparser: argparse.ArgumentParser = argparse.ArgumentParser()
argparser.add_argument(
    "-H",
    "--host",
    help="host of the server, default is localhost",
    default="localhost")
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
    def __init__(self) -> None:
        self.socket: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(5)
        self.users: list[User] = []

    def listen(self) -> None:
        """
        Accept connections from clients and create a new thread for each one
        """
        # while True:
        if True:
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
        server: Server = Server()
        print(f"Server is running on {host}:{port}")
        server.listen()
        server.listen()
        if verbose:
            print("Sending game...")
        server.game()
        server.stop()
        print("Server is stopped")
    except KeyboardInterrupt:
        print("\nStopping server...")
        server.stop()
        print("Server stopped")
        exit(0)
    except OSError:
        print("Address already in use")
        exit(1)
    except Exception as e:
        print("Fatal error: ", e)
        server.stop()
        exit(1)
