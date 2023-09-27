#!/usr/bin/env python3
# coding:utf-8

'''Server for the game'''

from typing import Tuple
from lib.game import game
from lib.network import recv_msg, send_msg, init_socket
from lib.user import User


class Server:
    '''Class that handle the network server for the game'''

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.socket = init_socket(host, port)
        self.users: list[User] = []

    def listen(self) -> User:
        '''
        Accept one connection from client
        '''
        conn, addr = self.socket.accept()
        print(f'Client connected from {addr}')
        user: User = User('', conn, addr, len(self.users)+1)
        self.users.append(user)

        # Useless but necessary
        # Send id to client and wait for 'OK'
        send_msg(conn, str(user.connection_id))
        if recv_msg(conn) == 'OK':
            print(f'Client {user.connection_id} connected')
            # Send 'READY' to client
            send_msg(conn, 'READY')
            # Wait for 'READY' from client
            if recv_msg(conn) != 'READY':
                print(f'Client {user.connection_id} not ready')
                user.stop()
                return None
        return user

    def stop(self) -> None:
        '''
        Stop the server
        '''
        for user in self.users:
            user.stop()
        self.socket.close()

    def unconnect(self, user: User) -> None:
        '''
        Unconnect the user
        '''
        self.users.remove(user)
        user.stop()

    def game(self, users: Tuple[User, User]) -> None:
        '''
        Start a game
        '''
        game(users)
