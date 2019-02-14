import json
import copy
from ctypes import c_uint32

from lib.move import GroundMove, StasisMove, AttackMove

class ClientConnection:

    def __init__(self, socket):
        self.sock = socket

    def objs_to_strs(self, lst):
        return list(map(str, lst))

    def print_map(self, state, game):
        display = copy.deepcopy(state['map'])
        for u in game.p1_state.values():
            display[u.y][u.x] = str(u)
        for u in game.p2_state.values():
            display[u.y][u.x] = str(u)

        for row in display:
            print(''.join(row))

        input()

    def units_to_dict(self, units):
        return [u.__dict__ for u in units.values()]

    def create_move(self, id, body):
        if isinstance(body, list) and len(body) > 1 and body[0] == 'DUPLICATE':
            return StasisMove(id, body[1])
        elif isinstance(body, list) and len(body) > 1 and body[0] == 'ATTACK':
            return AttackMove(id, body[1:])
        else:
            return GroundMove(id, body)

    def tick(self, game_state, me, them):
        d = {
            'map'         : [self.objs_to_strs(r) for r in game_state.grid],
            'my_units'    : self.units_to_dict(me),
            'their_units' : self.units_to_dict(them)
        }

        data = json.dumps(d).encode()
        self.sock.sendall('{:10}'.format(len(data)).encode())
        self.sock.sendall(data)

        size = int(self.sock.recv(10).decode())
        response = self.sock.recv(size).decode()

        self.print_map(d, game_state)

        j = json.loads(response)

        return [(k, self.create_move(k, v)) for k, v in j]
