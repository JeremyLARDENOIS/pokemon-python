#!/usr/bin/env python3
# coding:utf-8

'''Client for the game'''

import sys
import socket
import argparse
from typing import Optional
from lib.network import send_msg, recv_msg

argparser: argparse.ArgumentParser = argparse.ArgumentParser()
argparser.add_argument(
    "-H",
    "--host",
    help="host of the server, default is localhost",
    default="localhost")
argparser.add_argument(
    "-p",
    "--port",
    help="port of the server",
    type=int,
    default=3333)
argparser.add_argument(
    "-v",
    "--verbose",
    help="increase output verbosity",
    action="store_true")
args = argparser.parse_args()


class Client:
    """Class that handle the network client for the game"""

    def __init__(self, host: str, port: int) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((host, port))
        except ConnectionRefusedError:
            print("ERROR: Connection refused")
            sys.exit(1)
        self.connection_id: Optional[int] = None

    def send(self, msg: str) -> None:
        """Send a message in the socket"""
        send_msg(self.socket, msg)

    def recv(self) -> str:
        """Get a string from the socket"""
        return recv_msg(self.socket)

    def stop(self) -> None:
        """Stop the client socket"""
        if self.socket:
            self.socket.close()

    def get_id(self) -> None:
        """
        Get the id of the client
        Useless but necessary
        """
        self.connection_id = int(self.recv())
        print(f"Your id is {self.connection_id}")
        self.send("OK")

    def ready(self) -> None:
        """
        Wait for the client to be ready
        Useless but necessary
        """
        if self.recv() == "READY":
            self.send("READY")

    def communicate(self) -> None:
        """
        Communicate with the server
        """
        print("Starting communication")
        status = recv_msg(self.socket)
        # while ((status != "") and (status != "STOP")):
        while status not in ("", "STOP"):
            if status == "READ":  #  If he wants to print something
                send_msg(self.socket, "OK")          # We answer "OK"
                msg = recv_msg(self.socket)        # He send the message
                print(msg)              # We print it
                if msg != "":         # And if it was ok
                    send_msg(self.socket, "OK")       # We answer "OK"
            if status == "WRITE":     # If we wants some information
                msg = input('-> ')      # User enter a message
                send_msg(self.socket, msg)           # And we send it
                # status = recv_msg()
            if status == "OK":        # If we receive "OK"
                send_msg(self.socket, "OK")          # We answer "OK"
            # Write v2 : allow to send message in same time that other user
            if status == "WRITE2":
                msg = input('-> ')      # User enter a message
                # We say that we are ok for sending
                send_msg(self.socket, "OK")
            if status == "SEND":      # If he wants the message,
                send_msg(self.socket, msg)           # We send it

            status = recv_msg(self.socket)


if __name__ == "__main__":
    try:
        client: Client = Client(args.host, args.port)
        if args.verbose:
            print(f"Connected to server on {args.host}:{args.port}")
        client.get_id()
        client.ready()
        client.communicate()
        # Stop the client and return 0
        client.stop()
        sys.exit(0)
    except KeyboardInterrupt:
        print("\nStopping client...")
        client.stop()
        sys.exit(0)
