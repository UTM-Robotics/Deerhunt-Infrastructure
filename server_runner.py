#!/usr/bin/env python3

import argparse
import socket

from pyglet.window import key

from snake import Snake
from render import SnakeRenderer

from controller import * 

parser = argparse.ArgumentParser()
parser.add_argument('port', type=int,
                    help='The port to listen on')
parser.add_argument('--keyboard', dest='keyboard',
                    action='store_const', const=True, default=False,
                    help='Use this to control one player via keys.')
args = parser.parse_args()

key_handler = key.KeyStateHandler()

sock = socket.socket()
host = socket.gethostname()
sock.bind((host, args.port))

sock.listen(2)

print('Waiting for client 1...')
conn, addr = sock.accept()
controller_one = NetworkedController(conn)

if args.keyboard:
    controller_two = KeyboardController(key_handler,
                                        key.LEFT,
                                        key.RIGHT,
                                        key.UP,
                                        key.DOWN)
else:
    print('Waiting for client 2...')
    conn, addr = sock.accept()
    controller_two = NetworkedController(conn)

game = Snake(controller_one, controller_two)

MAP_WIDTH  = 100
MAP_HEIGHT = 100
renderer = SnakeRenderer(MAP_WIDTH, MAP_HEIGHT, game, key_handler)

@renderer.window.event
def on_draw():
    renderer.window.clear()

    player_one = renderer.game.player_one
    player_two = renderer.game.player_two

    renderer.draw_player_one(player_one.get_visible_segments())
    renderer.draw_player_two(player_two.get_visible_segments())
    renderer.draw_food(*renderer.game.current_food)

renderer.run()
sock.close()
