from game import Game
from units import Unit, MeleeUnit, RangedUnit
from lib.move import GroundMove, StasisMove, AttackMove

class GridFighters(Game):

    def __init__(self, player_one_connection, player_two_connection, map_file):
        self.grid = map_file

        self.next_id = 0
        self.currently_duplicating = {}
        self.all_units = {}

        self.p1_conn = player_one_connection
        self.p2_conn = player_two_connection

        self.p1_state = {
            'units': {}
        }
        self.p2_state = {
            'units': {}
        }

        self.add_unit(self.p1_state, MeleeUnit(2, 1))
        self.add_unit(self.p2_state, MeleeUnit(2, 3))

    def add_unit(self, player, unit):
        unit.id = self.next_id
        player['units'][str(self.next_id)] = unit
        self.next_id += 1

        self.all_units[f'{unit.x},{unit.y}'] = unit

    def verify_response(self, moves, player_state, enemy_units):
        potential_moves = {}
        move_type = {}
        for k, v in moves:
            if isinstance(player_state['units'][k], Unit):
                if player_state['units'][k].is_duplicating():
                    return False

                if k in move_type and move_type[k] != type(v):
                    return False

                potential_moves[k] = potential_moves.get(k, 0) + v.len()
                move_type[k] = type(v)

            x, y = player_state['units'][k].pos_tuple()

            if isinstance(v, GroundMove) and not v.valid_path(self.grid, x, y):
                return False
            elif isinstance(v, AttackMove) and (v.blocked(self.grid, x, y) or \
                 self.get_matching_unit(x, y, enemy_units, v) is None):
                return False
            elif isinstance(v, StasisMove) and not player_state['units'][k].can_duplicate():
                return False

        for k, v in potential_moves.items():
            if isinstance(player_state['units'][k], MeleeUnit) and v < 0 and v > 2:
                return False
            elif isinstance(player_state['units'][k], RangedUnit) and v < 0 and v > 1:
                return False

        return True

    def get_matching_unit(self, x, y, units, attack):
        rx, ry = attack.get_relative_moves()

        x += rx
        y += ry

        return self.all_units.get(f'{x},{y}', None)

    def make_moves(self, moves, player_state, oppenent_state):
        for k, v in moves:
            if isinstance(v, GroundMove):
                m = v.get_relative_moves()
                player_state['units'][k].set_relative_location(*m)
            elif isinstance(v, AttackMove):
                x, y = player_state['units'][k].pos_tuple()
                rx, ry = v.get_relative_moves()
                uid = str(self.all_units[f'{x+rx},{y+ry}'].id)
                del oppenent_state['units'][uid]
                del self.all_units[f'{x+rx},{y+ry}']
            elif isinstance(v, StasisMove):
                self.currently_duplicating[k] = player_state['units'][k].start_duplication()
            

    def tick_player(self, conn, current, opponent, name=''):
        moves = conn.tick(self, current, opponent)
        print(name, ':', moves)
        if self.verify_response(moves, current, opponent['units']):
            self.make_moves(moves, current, opponent)

    def tick(self):
        for k, unit in self.currently_duplicating.items():
            unit.duplication_status -= 1
            if unit.duplication_status == 0:
                # TODO: Actually make two units
                del self.currently_duplicating[k]

        self.tick_player(self.p1_conn, self.p1_state, self.p2_state, 'p1')
        self.tick_player(self.p2_conn, self.p2_state, self.p1_state, 'p2')
