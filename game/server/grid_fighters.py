from game import Game
from units import Unit, MeleeUnit, RangedUnit
from lib.move import GroundMove, StasisMove, AttackMove, Move
from lib.tiles import GroundTile, WallTile
from copy import deepcopy

class GridFighters(Game):

    def __init__(self, player_one_connection, player_two_connection, map_file):
        self.next_id = 0
        self.currently_duplicating = {}
        self.all_units = {}

        self.p1_conn = player_one_connection
        self.p2_conn = player_two_connection

        self.p1_state = {}
        self.p2_state = {}

        top = [line.rstrip() for line in map_file]
        bottom = deepcopy(top)
        bottom = [row[::-1] for row in bottom]
        bottom.reverse()

        self.grid = self.build_grid(top, self.p1_state, 0) + self.build_grid(bottom, self.p2_state, len(top))

    def build_grid(self, lines, player, base_y):
        return [[self.create_tile_or_unit(lines[y][x], player, x, y, base_y) for x in range(len(lines[y]))] for y in range(len(lines))]

    def create_tile_or_unit(self, tile_code, player, x, y, base_y):
        if tile_code.lower() == 'x':
            return WallTile()
        elif tile_code.lower() == 'm':
            self.add_unit(player, MeleeUnit(x, y+base_y))
        elif tile_code.lower() == 'r':
            self.add_unit(player, RangedUnit(x, y+base_y))

        return GroundTile()

    def add_unit(self, player, unit):
        unit.id = self.next_id
        player[str(self.next_id)] = unit
        self.next_id += 1

        self.all_units[f'{unit.x},{unit.y}'] = unit

    def verify_response(self, moves, player_state, enemy_units):
        potential_moves = {}
        move_type = {}
        for k, v in moves:
            if isinstance(player_state[k], Unit):
                if player_state[k].is_duplicating():
                    return False

                if k in move_type and move_type[k] != type(v):
                    return False

                potential_moves[k] = potential_moves.get(k, 0) + v.len()
                move_type[k] = type(v)

            x, y = player_state[k].pos_tuple()

            if isinstance(v, GroundMove) and not v.valid_path(self.grid, x, y):
                return False
            elif isinstance(v, AttackMove) and (v.blocked(self.grid, x, y) or \
                 self.get_matching_unit(x, y, enemy_units, v) is None):
                return False
            elif isinstance(v, StasisMove) and not player_state[k].can_duplicate():
                return False

        for k, v in potential_moves.items():
            if isinstance(player_state[k], MeleeUnit) and v < 0 and v > 2:
                return False
            elif isinstance(player_state[k], RangedUnit) and v < 0 and v > 1:
                return False

        return True

    def get_matching_unit(self, x, y, units, attack):
        rx, ry = attack.get_relative_moves()

        x += rx
        y += ry

        return self.all_units.get(f'{x},{y}', None)

    def make_moves(self, moves, player_state, opponent_state):
        for k, v in moves:
            if isinstance(v, GroundMove):
                m = v.get_relative_moves()
                player_state[k].set_relative_location(*m)
            elif isinstance(v, AttackMove):
                x, y = player_state[k].pos_tuple()
                rx, ry = v.get_relative_moves()
                uid = str(self.all_units[f'{x+rx},{y+ry}'].id)
                try:
                    del opponent_state[uid]
                except KeyError:
                    # User tried to delete their own unit
                    pass

                del self.all_units[f'{x+rx},{y+ry}']
            elif isinstance(v, StasisMove):
                self.currently_duplicating[k] = (player_state, player_state[k].start_duplication(v.direction))
            

    def tick_player(self, conn, current, opponent, name=''):
        moves = conn.tick(self, current, opponent)
        print(name, ':', moves)
        if self.verify_response(moves, current, opponent):
            self.make_moves(moves, current, opponent)

    def can_duplicate_to(self, unit):
        dir = unit.stasis_direction
        x = unit.x
        y = unit.y
        x, y = Move.transform(x, y, dir)
        if isinstance(self.grid[y][x], GroundTile):
            return True

        return False

    def create_duplicate(self, unit):
        ret = None
        if isinstance(unit, MeleeUnit):
            ret = MeleeUnit(*Move.transform(unit.x, unit.y, unit.stasis_direction))
        elif isinstance(unit, Ranged):
            ret = RangedUnit(*Move.transform(unit.x, unit.y, unit.stasis_direction))

        return ret

    def tick(self):
        for k, (player, unit) in list(self.currently_duplicating.items()):
            unit.duplication_status -= 1
            if unit.duplication_status == 0:
                del self.currently_duplicating[k]
                if self.can_duplicate_to(unit):
                    self.add_unit(player, self.create_duplicate(unit))

        self.tick_player(self.p1_conn, self.p1_state, self.p2_state, 'p1')
        self.tick_player(self.p2_conn, self.p2_state, self.p1_state, 'p2')

