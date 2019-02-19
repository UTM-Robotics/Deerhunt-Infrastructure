from move import Move
from pprint import pprint

class GridPlayer:

    def __init__(self):
        self.counter = 0
        pass

    def tick(self, game_map, your_units, enemy_units, resources, turns_left):

        print("\n--------RESOURCES: {0} | TURNS LEFT: {1}--------".format(resources, turns_left))
        print(game_map.grid[12][2])
        moves = []
        first = your_units.get_unit('0')
        closest_node = game_map.closest_resources(first)
        current_pos = (first.x, first.y)
        print(closest_node, " | ", current_pos);
        if current_pos[0] != closest_node[0] or current_pos[1] != closest_node[1]:
            moves.append(first.ghetto_move(current_pos, closest_node))
        else:
            moves.append(first.mine())
        return moves
