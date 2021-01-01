from direction import Direction
from tiles import GroundTile, WallTile
from units import Unit


class Move:
    def transform(x, y, direction):
        if direction == 'UP'    : y -= 1
        if direction == 'DOWN'  : y += 1
        if direction == 'RIGHT' : x += 1
        if direction == 'LEFT'  : x -= 1
        return x, y

    def _get_relative_moves(lst):
        x = 0
        y = 0
        for m in lst:
            if isinstance(m, list):
                for n in m:
                    x, y = Move.transform(x, y, n)
            else:
                x, y = Move.transform(x, y, m)

        return x, y

    def _can_follow_path(self, lst, board, all_units, x, y):
        for m in lst:
            x, y = Move.transform(x, y, m)

            if all_units.get('{},{}'.format(x, y)) is not None:
                return False

            if isinstance(board[y][x], WallTile):
                return False

        return True

class AttackMove(Move):

    def __init__(self, unit, target):
        self.unit = unit
        self.target = target

    def len(self):
        return len(self.target)

    def get_relative_moves(self):
        return Move._get_relative_moves(self.target)

class StunMove(Move):

    def __init__(self, unit, target):
        self.unit = unit
        self.target = target

    def len(self):
        return len(self.target)

    def get_relative_moves(self):
        return Move._get_relative_moves(self.target)


class StasisMove(Move):

    def __init__(self, unit, direction, unit_type):
        self.unit = unit
        self.direction = direction
        self.unit_type = unit_type

    def len(self):
        return 0

    def free_spot(self, x, y, all_units, board):
        nx, ny = Move.transform(x, y, self.direction)
        if isinstance(board[ny][nx], WallTile):
            return False

        return '{},{}'.format(nx, ny) not in all_units


class GroundMove(Move):

    def __init__(self, unit, moves):
        self.unit = unit
        self.moves = moves

    def len(self):
        return len(self.moves)

    def get_dict(self):
        return {self.unit.id: self.moves}

    def valid_path(self, board, all_units, x, y):
        return self._can_follow_path(self.moves, board, all_units, x, y)
        
    def get_relative_moves(self):
        return Move._get_relative_moves(self.moves)


class MineMove(Move):

    def __init__(self, unit):
        self.unit = unit

    def len(self):
        return 0
