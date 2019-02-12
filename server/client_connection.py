import json
import copy

class ClientConnection:

    def __init__(self, socket):
        self.sock = socket

    def objs_to_strs(self, lst):
        return list(map(str, lst))

    def print_map(self, state, game):
        display = copy.deepcopy(state['map'])
        for u in game.p1_state['units'].values():
            display[u.y][u.x] = str(u)
        for u in game.p2_state['units'].values():
            display[u.y][u.x] = str(u)

        for row in display:
            print(''.join(row))

        input()

    def units_to_dict(self, units):
        return [u.__dict__ for u in units.values()]

    def tick(self, game_state, me, them):
        d = {
            'map'         : [self.objs_to_strs(r) for r in game_state.grid],
            'my_units'    : self.units_to_dict(me['units']),
            'their_units' : self.units_to_dict(them['units'])
        }
        self.sock.sendall(json.dumps(d).encode())

        response = self.sock.recv(1024).decode()

        self.print_map(d, game_state)

        return json.loads(response)
