from move import Move
from pprint import pprint

class GridPlayer:

    def __init__(self):
        self.counter = 0
        pass

    def tick(self, game_map, your_units, enemy_units, resources, turns_left):
        moves = []
        moves.append(Move('0', 'DOWN'))
        moves.append(Move('3', 'DOWN'))

        return moves
