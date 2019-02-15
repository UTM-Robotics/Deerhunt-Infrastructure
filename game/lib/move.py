from lib.direction import Direction
from lib.tiles import GroundTile, WallTile
from units import Unit


class Move:
    def transform(x, y, direction):
        if direction == 'UP'    : y -= 1
        if direction == 'DOWN'  : y += 1
        if direction == 'RIGHT' : x += 1
        if direction == 'LEFT'  : x -= 1
        return x, y

    def _get_relative_moves(self, lst):
        x = 0
        y = 0
        for m in lst:
            x, y = Move.transform(x, y, m)

        return x, y

    def _can_follow_path(self, lst, board, all_units, x, y):
        for m in lst:
            x, y = Move.transform(x, y, m)

            if all_units.get(f'{x},{y}') is not None:
                return False

            if not isinstance(board[y][x], GroundTile):
                return False

        return True

class AttackMove(Move):

    def __init__(self, unit, target):
        self.unit = unit
        self.target = target

    def len(self):
        return len(self.target)

    def blocked(self, grid, all_units, x, y):
        return not self._can_follow_path(self.target, grid, all_units, x, y)

    def get_relative_moves(self):
        return self._get_relative_moves(self.target)

class StasisMove(Move):

    def __init__(self, unit, direction):
        self.unit = unit
        self.direction = direction

    def len(self):
        return 0

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
        return self._get_relative_moves(self.moves)


class MineMove(Move):

    def __init__(self, unit, direction):
        self.unit = unit
        self.direction = direction

    def len(self):
        return 0
