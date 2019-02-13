from lib.direction import Direction

class Move:

    def __init__(self, unit, moves):
        self.unit = unit
        self.moves = moves

    def get_dict(self):
        return {self.unit.id: self.moves}

    def should_duplicate(self):
        if len(self.moves) > 0 and self.moves[0] == 'DUPLICATE':
            return True

        return False

    def get_relative_moves(self):
        x = 0
        y = 0
        for m in self.moves:
            if m == 'UP'    : x -= 1
            if m == 'DOWN'  : x += 1
            if m == 'RIGHT' : y += 1
            if m == 'LEFT'  : y -= 1

        return x, y
