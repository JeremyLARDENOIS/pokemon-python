#!/usr/bin/env python3
# coding:utf-8

'''Client for the game'''

import sys
import argparse
from lib.client import Client

argparser: argparse.ArgumentParser = argparse.ArgumentParser()
argparser.add_argument(
    '-H',
    '--host',
    help='host of the server, default is localhost',
    default='localhost')
argparser.add_argument(
    '-p',
    '--port',
    help='port of the server',
    type=int,
    default=3333)
argparser.add_argument(
    '-v',
    '--verbose',
    help='increase output verbosity',
    action='store_true')
args = argparser.parse_args()


if __name__ == '__main__':
    try:
        client: Client = Client(args.host, args.port)
        if args.verbose:
            print(f'Connected to server on {args.host}:{args.port}')
        client.get_id()
        client.ready()
        client.communicate()
        # Stop the client and return 0
        client.stop()
        sys.exit(0)
    except KeyboardInterrupt:
        print('\nStopping client...')
        client.stop()
        sys.exit(0)
