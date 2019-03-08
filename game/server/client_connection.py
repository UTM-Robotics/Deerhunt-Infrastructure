import json
import copy
from ctypes import c_uint32

from move import GroundMove, StasisMove, AttackMove, MineMove

class ClientConnection:

    def __init__(self, socket, player_name, verbose=False):
        self.sock = socket
        self.name = player_name
        self.verbose = verbose
        self.vision_range = 4

    def objs_to_strs(self, lst):
        return list(map(str, lst))

    def print_map(self, state, game):
        display = copy.deepcopy(state['map'])
        for u in game.p1_units.values():
            display[u.y][u.x] = str(u)
        for u in game.p2_units.values():
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
        elif isinstance(body, list) and len(body) > 0 and body[0] == 'MINE':
            return MineMove(id)
        else:
            return GroundMove(id, body)

    def filter_fog_of_war(self, current, opponent):
        ret = copy.deepcopy(opponent)
        for o_id, o_unit in list(ret.items()):
            should_include = False
            for id, unit in current.items():
                if o_unit.x > unit.x-self.vision_range and o_unit.x < unit.x+self.vision_range and \
                   o_unit.y > unit.y-self.vision_range and o_unit.y < unit.y+self.vision_range:
                    should_include = True

            if not should_include:
                del ret[o_id]

        return ret


    def tick(self, game_state, me, them, resources, turns):
        try:
            d = {
                'map'         : [self.objs_to_strs(r) for r in game_state.grid],
                'my_units'    : self.units_to_dict(me),
                'their_units' : self.units_to_dict(self.filter_fog_of_war(me, them)),
                'my_resources': resources[self.name],
                'turns_left'  : turns
            }

            data = json.dumps(d).encode()
            self.sock.sendall('{:10}'.format(len(data)).encode())
            self.sock.sendall(data)

            size = int(self.sock.recv(10).decode())
            response = self.sock.recv(size).decode()

            if self.verbose:
                self.print_map(d, game_state)

            j = json.loads(response)

            moves = [(str(k), self.create_move(k, v)) for k, v in j]

            if self.verbose:
                print(self.name, ':', moves)

            return moves
        except:
            return []
