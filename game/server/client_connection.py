import json
import copy
from ctypes import c_uint32

from move import GroundMove, StasisMove, AttackMove, MineMove, StunMove
from units import MELEE_UNIT, WORKER_UNIT

#String constants for all available commands
CMD_DUPLICATE_WORKER = 'DUPLICATE_W'
CMD_DUPLICATE_MELEE = 'DUPLICATE_M'
CMD_ATTACK = 'ATTACK'
CMD_MINE = 'MINE'
CMD_STUN = 'STUN'


class ClientConnection:
    """
    ClientConnection manages the connection with clients. Sends the required data to 
    the socket as well as parsing the data received.
    """

    def __init__(self, socket, player_name, verbose=False):
        self.sock = socket
        self.name = player_name
        self.verbose = verbose
        self.vision_range = 4

    #print_map prints a new copy of the map with the new state and waits for user input to continue. Shown if app is verbose.
    def print_map(self, state, game):
        display = copy.deepcopy(state['map'])
        #Adds units to the copied map
        for u in game.p1_units.values():
            display[u.y][u.x] = str(u)
        for u in game.p2_units.values():
            display[u.y][u.x] = str(u)

        #Prints each row
        for row in display:
            print(''.join(row))

        input()

    #units_to_dict returns a list of each unit as a dictionary
    def units_to_dict(self, units):
        return [u.__dict__ for u in units.values()]

    #Create move parses the data retrieved in the response body and returns the appropriate move.
    def create_move(self, id, body):
        try:
            if body[0] == CMD_DUPLICATE_MELEE:
                return StasisMove(id, body[1], MELEE_UNIT)
            if body[0] == CMD_DUPLICATE_WORKER:
                return StasisMove(id, body[1], WORKER_UNIT)
            if body[0] == CMD_ATTACK:
                return AttackMove(id, body[1:])
            if body[0] == CMD_STUN:
                return StunMove(id, body[1:])
            if body[0] == CMD_MINE:
                return MineMove(id)
            return GroundMove(id, body)
        except:
            #Happens if not enough data is send in body.
            return

    #filter_fog_of_war updates what each player can see on the board given each units vision
    def filter_fog_of_war(self, current, opponent):
        #Coppies the opponents units and filters through them
        ret = copy.deepcopy(opponent)
        for o_id, o_unit in list(ret.items()):
            should_include = False
            #If you have a unit that can see o_unit then keep it
            for id, unit in current.items():
                if o_unit.x > unit.x-self.vision_range and o_unit.x < unit.x+self.vision_range and \
                   o_unit.y > unit.y-self.vision_range and o_unit.y < unit.y+self.vision_range:
                    should_include = True

            #If no unit sees o_unit remove it from the visible units
            if not should_include:
                del ret[o_id]

        #Returns a list of visible enemy units
        return ret


    #tick sends the current game state and retrieves a list of moves to execute from the client
    def tick(self, game_state, me, them, resources, turns):
        try:
            #Sends the state to the client
            d = {
                'map'         : [list(map(str, r)) for r in game_state.grid],
                'my_units'    : self.units_to_dict(me),
                'their_units' : self.units_to_dict(self.filter_fog_of_war(me, them)),
                'my_resources': resources[self.name],
                'turns_left'  : turns
            }

            data = json.dumps(d).encode()
            self.sock.sendall('{:10}'.format(len(data)).encode())
            self.sock.sendall(data)

            #Retrieve the response and print the current map before the move
            size = int(self.sock.recv(10).decode())
            response = self.sock.recv(size).decode()

            if self.verbose:
                self.print_map(d, game_state)

            j = json.loads(response)

            #Parse to commands to unit moves and print them
            moves = [(str(k), self.create_move(k, v)) for k, v in j]

            if self.verbose:
                print(self.name, ':', moves)

            return moves
        except:
            return []
