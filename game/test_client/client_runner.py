#!/usr/bin/env python3

import argparse
import socket
# import sys
from controller import NetworkedController
from grid_player import GridPlayer

parser = argparse.ArgumentParser()
parser.add_argument('host', type=str, help='The host to connect to')
parser.add_argument('port', type=int, help='The port to listen on')
args = parser.parse_args()

sock = socket.socket()
sock.connect((args.host, args.port))

player = GridPlayer()
controller = NetworkedController(sock, player)

while controller.tick():
    pass

sock.close()
