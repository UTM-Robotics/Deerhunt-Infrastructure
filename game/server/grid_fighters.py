import json
from game import Game
from units import Unit, MeleeUnit, WorkerUnit, MELEE_UNIT, WORKER_UNIT
from move import GroundMove, StasisMove, AttackMove, Move, MineMove, StunMove
from tiles import GroundTile, WallTile, ResourceTile
from copy import deepcopy

class GridFighters(Game):

    def __init__(self, player_one_connection, player_two_connection, map_file):
        self.next_id = 0
        self.currently_duplicating = {}
        self.currently_mining = {}
        self.currently_stunned = {}
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

        self.set_unit(unit.x, unit.y, unit)

    def move_unit(self, x, y, unit):
        del self.all_units['{},{}'.format(x, y)]
        self.set_unit(unit.x, unit.y, unit)

    def set_unit(self, x, y, unit):
        self.all_units['{},{}'.format(x, y)] = unit

    def get_unit(self, x, y):
        return self.all_units['{},{}'.format(x, y)]

    def del_unit(self, x, y):
        del self.all_units['{},{}'.format(x,y)]

    def verify_move(self, k, v, player_state, player_resources, enemy_units, moved_units):
        if k not in player_state:
            print('ERROR: Cannot move enemy unit: {}'.format(k))
            return False

        if isinstance(player_state[k], Unit):
            if player_state[k].is_duplicating():
                print('ERROR: {} cannot act while duplicating'.format(k))
                return False

            if player_state[k].is_mining():
                print('ERROR: {} cannot act while mining'.format(k))
                return False

            if player_state[k].is_stunned():
                print('ERROR: {} cannot act while stunned'.format(k))
                return False

            if k in moved_units:
                print('ERROR: Cannot make multiple actions for unit {}'.format(k))
                return False

            moved_units.add(k)

        x, y = player_state[k].pos_tuple()

        if isinstance(v, GroundMove) and (not v.valid_path(self.grid, self.all_units, x, y) or v.len() < 0 or v.len() > 1):
            print('ERROR: Invalid path for unit {}'.format(k))
            return False
        elif isinstance(v, AttackMove) and (self.get_matching_unit(x, y, v) is None or v.len() < 0 or v.len() > 1):
            print('ERROR: Unit {} cannot attack there'.format(k))
            return False
        elif isinstance(v, StunMove) and (self.get_matching_unit(x, y, v) is None or v.len() < 0 or v.len() > 2):
            print('ERROR: Unit {} cannot stun there'.format(k))
            return False
        elif isinstance(v, StasisMove) and (not player_state[k].can_duplicate(player_resources, v.unit_type)
                                            or not v.free_spot(x, y, self.all_units, self.grid)):
            print('ERROR: Unit {} cannot duplicate now'.format(k))
            return False
        elif isinstance(v, MineMove) and (not player_state[k].can_mine() or not self.is_mining_resource(x, y)):
            print('ERROR: Unit {} cannot mine now'.format(k))
            return False

        return True

    def is_mining_resource(self, x, y):
        return isinstance(self.grid[y][x], ResourceTile)
    
    def get_matching_unit(self, x, y, attack):
        rx, ry = attack.get_relative_moves()

        x += rx
        y += ry

        return self.all_units.get('{},{}'.format(x, y), None)

    def make_move(self, k, v, player_state, player_name, opponent_state):
        if isinstance(v, GroundMove):
            m = v.get_relative_moves()
            x, y = player_state[k].pos_tuple()
            player_state[k].set_relative_location(self.all_units, *m)
            self.move_unit(x, y, player_state[k])
        elif isinstance(v, AttackMove):
            x, y = player_state[k].pos_tuple()
            rx, ry = v.get_relative_moves()
            uid = str(self.get_unit(x+rx, y+ry).id)
            try:
                del opponent_state[uid]
            except KeyError:
                # User tried to delete their own unit
                pass

            self.del_unit(x+rx, y+ry)
        elif isinstance(v, StasisMove):
            self.currently_duplicating[k] = (
                player_state, player_state[k].start_duplication(v.direction, v.unit_type))
            if v.unit_type == MELEE_UNIT:
                self.resources[player_name] -= player_state[k].melee_cost
            else:
                self.resources[player_name] -= player_state[k].worker_cost
        elif isinstance(v, MineMove):
            self.currently_mining[k] = (
                player_name, player_state[k].start_mining())
        elif isinstance(v, StunMove):
            x, y = player_state[k].pos_tuple()
            rx, ry = v.get_relative_moves()
            uid = str(self.get_unit(x+rx, y+ry).id)
            try:
                opponent_state[uid].stun()
                self.resources[player_name] -= player_state[k].stun_cost
            except:
                pass

    def tick_player(self, conn, current, opponent, name, turns):
        moves = conn.tick(self, current, opponent, self.resources, turns)

        moved_units = set()
        for m in moves:
            k, v = m
            if self.verify_move(k, v, current, self.resources[name], opponent, moved_units):
                self.make_move(k, v, current, name, opponent)


    def can_duplicate_to(self, unit):
        dir = unit.stasis_direction
        x = unit.x
        y = unit.y
        x, y = Move.transform(x, y, dir)
        if isinstance(self.grid[y][x], GroundTile):
            return True

        return False

    def create_duplicate(self, unit):
        if unit.duplication_unit == MELEE_UNIT:
            return MeleeUnit(*Move.transform(unit.x, unit.y, unit.stasis_direction))
        else:
            return WorkerUnit(*Move.transform(unit.x, unit.y, unit.stasis_direction))

    def has_lost(self, enemy_units):
        return len(enemy_units) == 0

    def json_str(self):
        display = deepcopy(self.grid)
        for u in self.p1_units.values():
            display[u.y][u.x] = u
        for u in self.p2_units.values():
            display[u.y][u.x] = u.string().upper()

        inner = lambda r: '[{}]'.format(','.join(map(lambda x: (x if isinstance(x, str) else x.string()), r)))
        return '[{}]'.format(','.join(map(inner, display)))

    def print_map(self, p1_name, p2_name):
        j = json.dumps({
            'map': self.json_str(),
            'p1_resources': self.resources[p1_name],
            'p2_resources': self.resources[p2_name]
            })
        print('MAP:{}'.format(j))

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
        self.print_map(self.p1_conn.name, self.p2_conn.name)

        if self.has_lost(self.p2_units):
            return self.p1_conn.name

        self.tick_player(self.p2_conn, self.p2_units, self.p1_units, self.p2_conn.name, turns)
        self.print_map(self.p1_conn.name, self.p2_conn.name)

        if self.has_lost(self.p1_units):
            return self.p2_conn.name

