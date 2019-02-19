from move import Move
from pprint import pprint

class GridPlayer:

    def __init__(self):
        self.counter = 0
        pass

    def tick(self, game_map, your_units, enemy_units, resources, turns_left):
        moves = []
        #print("--------{0} TURNS LEFT--------".format(turns_left))
        first = your_units.get_unit('0')
        closest_node = game_map.closest_resources(first)
        current_pos = first.position
        if current_pos != closest_node:
            moves.append(first.ghetto_move(current_pos, closest_node))
        elif current_post == closest_node:
            moves.append(first.Move('MINE'))
        return moves
