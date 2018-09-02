import json
import socket

from pyglet.window import key
from directions import Direction
from snakeplayer import SnakePlayer

class Controller:
    def tick(self, game, my_player: SnakePlayer,
           their_player: SnakePlayer) -> Direction:
        raise NotImplementedError('Should have implemented this')

class NetworkedController(Controller):
    def __init__(self, conn: socket):
        self.conn = conn

    def tick(self, game, my_player: SnakePlayer,
           their_player: SnakePlayer) -> Direction:
        # TODO timeout after N seconds

        self.conn.send(json.dumps({
            'my_segments': my_player.segments,
            'their_segments': their_player.segments,
            'food_point': game.current_food,
        }).encode('utf-8'))

        response = self.conn.recv(8)

        while len(response) == 0:
            print('Zero response!')
            response = self.conn.recv(8)

        if response == b'left':
            return Direction.LEFT
        elif response == b'right':
            return Direction.RIGHT
        elif response == b'up':
            return Direction.UP
        elif response == b'down':
            return Direction.DOWN
        else:
            print('Invalid response from client: ' + str(response))
            exit(1)

class KeyboardController(Controller):
    def __init__(self, key_handler,
               left_key, right_key, up_key, down_key):
        self.key_handler = key_handler
        self.direction_map = {
            left_key:  Direction.LEFT,
            right_key: Direction.RIGHT,
            up_key:    Direction.UP,
            down_key:  Direction.DOWN,
        }
        # Initial direction
        self.direction = Direction.DOWN

    def _get_new_direction(self):
        for key,direction in self.direction_map.items():
            if self.key_handler[key]:
                return direction
        return self.direction

    def tick(self, game, my_player: SnakePlayer,
           their_player: SnakePlayer) -> Direction:
        self.direction = self._get_new_direction()
        return self.direction
