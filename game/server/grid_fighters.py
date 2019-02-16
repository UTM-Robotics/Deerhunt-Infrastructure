from game import Game
from units import Unit, MeleeUnit, WorkerUnit
from lib.move import GroundMove, StasisMove, AttackMove, Move, MineMove
from lib.tiles import GroundTile, WallTile, ResourceTile
from copy import deepcopy

class GridFighters(Game):

    def __init__(self, player_one_connection, player_two_connection, map_file):
        self.next_id = 0
        self.currently_duplicating = {}
        self.currently_mining = {}
        self.all_units = {}

        self.p1_conn = player_one_connection
        self.p2_conn = player_two_connection

        self.p1_units = {}
        self.p2_units = {}
        self.resources = {
            self.p1_conn.name: 0,
            self.p2_conn.name: 0
        }

        top = [line.rstrip() for line in map_file]
        bottom = deepcopy(top[:-1])
        bottom = [row[::-1] for row in bottom]
        bottom.reverse()

        self.grid = self.build_grid(top, self.p1_units, 0) + self.build_grid(bottom, self.p2_units, len(top))

    def build_grid(self, lines, player, base_y):
        return [[self.create_tile_or_unit(lines[y][x], player, x, y, base_y) \
            for x in range(len(lines[y]))] \
            for y in range(len(lines))]

    def create_tile_or_unit(self, tile_code, player, x, y, base_y):
        if tile_code.lower() == 'x':
            return WallTile()
        elif tile_code.lower() == 'r':
            return ResourceTile()
        elif tile_code.lower() == 'm':
            self.add_unit(player, MeleeUnit(x, y+base_y))
        elif tile_code.lower() == 'w':
            self.add_unit(player, WorkerUnit(x, y+base_y))

        return GroundTile()

    def add_unit(self, player, unit):
        unit.id = self.next_id
        player[str(self.next_id)] = unit
        self.next_id += 1

        self.all_units[f'{unit.x},{unit.y}'] = unit

    def verify_response(self, moves, player_state, player_resources, enemy_units):
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

            if isinstance(v, GroundMove) and not v.valid_path(self.grid, self.all_units, x, y):
                return False
            elif isinstance(v, AttackMove) and (v.blocked(self.grid, self.all_units, x, y) or \
                 self.get_matching_unit(x, y, enemy_units, v) is None):
                return False
            elif isinstance(v, StasisMove) and not player_state[k].can_duplicate(player_resources):
                return False
            elif isinstance(v, MineMove) and (not player_state[k].can_mine() or not self.is_mining_resource(x, y, v.direction)):
                return False

        for k, v in potential_moves.items():
            if isinstance(player_state[k], MeleeUnit) and v < 0 and v > 2:
                return False
            elif isinstance(player_state[k], WorkerUnit) and v < 0 and v > 1:
                return False

        return True

    def is_mining_resource(self, x, y, direction):
        x, y = Move.transform(x, y, direction)
        return isinstance(self.grid[y][x], ResourceTile)
    

    def get_matching_unit(self, x, y, units, attack):
        rx, ry = attack.get_relative_moves()

        x += rx
        y += ry

        return self.all_units.get(f'{x},{y}', None)

    def make_moves(self, moves, player_state, player_name, opponent_state):
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
            elif isinstance(v, MineMove):
                self.currently_mining[k] = (player_name, player_state[k].start_mining(v.direction))
            

    def tick_player(self, conn, current, opponent, name, turns):
        moves = conn.tick(self, current, opponent, self.resources, turns)
        if self.verify_response(moves, current, self.resources[name], opponent):
            self.make_moves(moves, current, name, opponent)

    def can_duplicate_to(self, unit):
        dir = unit.stasis_direction
        x = unit.x
        y = unit.y
        x, y = Move.transform(x, y, dir)
        if isinstance(self.grid[y][x], GroundTile):
            return True

        return False

    def create_duplicate(self, unit):
        return MeleeUnit(*Move.transform(unit.x, unit.y, unit.stasis_direction))

    def has_lost(self, enemy_units):
        return len(enemy_units) == 0

    def tick(self, turns):
        for k, (player, unit) in list(self.currently_duplicating.items()):
            unit.duplication_status -= 1
            if unit.duplication_status == 0:
                del self.currently_duplicating[k]
                if self.can_duplicate_to(unit):
                    self.add_unit(player, self.create_duplicate(unit))

        for k, (p_name, unit) in list(self.currently_mining.items()):
            unit.mining_status -= 1
            if unit.mining_status == 0:
                del self.currently_mining[k]
                self.resources[p_name] += 75

        self.tick_player(self.p1_conn, self.p1_units, self.p2_units, self.p1_conn.name, turns)
        if self.has_lost(self.p2_units):
            return self.p1_conn.name
        self.tick_player(self.p2_conn, self.p2_units, self.p1_units, self.p2_conn.name, turns)
        if self.has_lost(self.p1_units):
            return self.p2_conn.name
