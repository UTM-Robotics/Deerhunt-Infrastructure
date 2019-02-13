from lib.direction import Direction
from lib.tiles import GroundTile, WallTile
from units import Unit


class Move:
    def _get_relative_moves(self, lst):
        x = 0
        y = 0
        for m in lst:
            if m == 'UP'    : y -= 1
            if m == 'DOWN'  : y += 1
            if m == 'RIGHT' : x += 1
            if m == 'LEFT'  : x -= 1

        return x, y

    def _can_follow_path(self, lst, board, x, y):
        for m in lst:
            if m == 'UP'    : y -= 1
            if m == 'DOWN'  : y += 1
            if m == 'RIGHT' : x += 1
            if m == 'LEFT'  : x -= 1

            if isinstance(board[y][x], WallTile):
                return False

        return True

class AttackMove(Move):

    def __init__(self, unit, target):
        self.unit = unit
        self.target = target

    def len(self):
        return len(self.target)

    def blocked(self, grid, x, y):
        return not self._can_follow_path(self.target, grid, x, y)

    def get_relative_moves(self):
        return self._get_relative_moves(self.target)

class StasisMove(Move):

    def __init__(self, unit):
        self.unit = unit

class GroundMove(Move):

    def __init__(self, unit, moves):
        self.unit = unit
        self.moves = moves

    def len(self):
        return len(self.moves)

    def get_dict(self):
        return {self.unit.id: self.moves}

    def valid_path(self, board, x, y):
        return self._can_follow_path(self.moves, board, x, y)
        
    def get_relative_moves(self):
        return self._get_relative_moves(self.moves)
