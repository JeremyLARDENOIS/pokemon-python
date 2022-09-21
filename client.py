#!/usr/bin/env python3

from lib.network import send_msg, recv_msg
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
args: argparse.ArgumentParser = argparser.parse_args()

host: str = args.host
port: int = args.port
verbose = args.verbose


class Client:
    def __init__(self, host: str, port: int) -> None:
        self.socket: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.id: int = None

    def send(self, msg: str) -> None:
        send_msg(self.socket, msg)

    def recv(self) -> str:
        return recv_msg(self.socket)

    def stop(self) -> int:
        try:
            self.socket.close()
            return 0
        except:
            return 1

    def get_id(self) -> None:
        """
        Get the id of the client
        Useless but necessary
        """
        self.id: int = int(self.recv())
        print(f"Your id is {self.id}")
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
        while ((status != "") and (status != "STOP")):
            if (status == "READ"):  #  If he wants to print something
                send_msg(self.socket, "OK")          # We answer "OK"
                msg = recv_msg(self.socket)        # He send the message
                print(msg)              # We print it
                if (msg != ""):         # And if it was ok
                    send_msg(self.socket, "OK")       # We answer "OK"
            if (status == "WRITE"):     # If we wants some information
                msg = input('-> ')      # User enter a message
                send_msg(self.socket, msg)           # And we send it
                # status = recv_msg()
            if (status == "OK"):        # If we receive "OK"
                send_msg(self.socket, "OK")          # We answer "OK"
            if (status == "WRITE2"):    # Write v2 : allow to send message in same time that other user
                msg = input('-> ')      # User enter a message
                # We say that we are ok for sending
                send_msg(self.socket, "OK")
            if (status == "SEND"):      # If he wants the message,
                send_msg(self.socket, msg)           # We send it

            status = recv_msg(self.socket)


if __name__ == "__main__":
    try:
        client: Client = Client(host, port)
        if verbose:
            print(f"Connected to server on {host}:{port}")
        client.get_id()
        client.ready()
        client.communicate()
        # Stop the client and return 0 if everything is ok
        exit(client.stop())
    except KeyboardInterrupt:
        print("\nStopping client...")
        exit(client.stop())
    except Exception as e:
        print("Fatal error: ", e)
        exit(client.stop() + 1)
