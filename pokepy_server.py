#!/usr/bin/env python3
# coding:utf-8

'''Server for the game'''

import argparse
import sys
from lib.server import Server
from lib.user import User

argparser: argparse.ArgumentParser = argparse.ArgumentParser()
argparser.add_argument(
    '-H',
    '--host',
    help='host of the server, default is localhost',
    default='0.0.0.0')
argparser.add_argument(
    '-p',
    '--port',
    help='port to listen',
    type=int,
    default=3333)
argparser.add_argument(
    '-v',
    '--verbose',
    help='increase output verbosity',
    action='store_true')
args = argparser.parse_args()

host: str = args.host
port: int = args.port
verbose = args.verbose


##################################MAIN#############################################
if __name__ == '__main__':
    try:
        server: Server = Server(host, port)
        print(f'Server is running on {host}:{port}')
        users: list[User] = []
        while True:
            user = server.listen()
            if user:
                users.append(user)
            if len(users) == 2:
                user1, user2 = users
                users = []
                if verbose:
                    print('2 users connected')

            if verbose:
                print('Sending game...')
            ###
            # Put this part in a thread
            server.game((user1, user2))
            user1.stop()
            user2.stop()
            ###
    except KeyboardInterrupt:
        print('\nStopping server...')
        server.stop()
        print('Server stopped')
        sys.exit(0)
    except OSError:
        print('Address already in use')
        sys.exit(1)
