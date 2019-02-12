#!/usr/bin/env python3

import argparse
import socket

from grid_fighters import GridFighters
from client_connection import ClientConnection
from tiles import WallTile, GroundTile

parser = argparse.ArgumentParser()
parser.add_argument('port', type=int, help='The port to listen on')
args = parser.parse_args()

sock = socket.socket()
host = socket.gethostname()
sock.bind((host, args.port))

sock.listen(2)

print('Waiting for client 1...')
conn1, addr1 = sock.accept()
p1 = ClientConnection(conn1)

print('Waiting for client 2...')
conn2, addr2 = sock.accept()
p2 = ClientConnection(conn2)

map = [
    [WallTile(), WallTile(), WallTile(), WallTile(), WallTile()],
    [WallTile(), GroundTile(), GroundTile(), GroundTile(), WallTile()],
    [WallTile(), GroundTile(), GroundTile(), GroundTile(), WallTile()],
    [WallTile(), GroundTile(), GroundTile(), GroundTile(), WallTile()],
    [WallTile(), WallTile(), WallTile(), WallTile(), WallTile()]
]
game = GridFighters(p1, p2, map)

while True:
    game.tick()

sock.close()
