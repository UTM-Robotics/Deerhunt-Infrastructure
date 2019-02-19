from move import Move
from pprint import pprint

class GridPlayer:

    def __init__(self):
        self.counter = 0
        pass

    def tick(self, game_map, your_units, enemy_units, resources, turns_left):

        print("\n--------RESOURCES: {0} | TURNS LEFT: {1}--------".format(resources, turns_left))

        moves = []

        all_units = your_units.get_all_unit_ids()
        for ids in all_units:
            print(ids, " : ", your_units.get_unit(ids).type)

        first = your_units.get_unit('0')
        closest_node = game_map.closest_resources(first)

        s_path = first.bfs(game_map, closest_node)

        print(first.x, first.y)
        print("close: ", closest_node)
        print(s_path)
        print("---")
        if s_path == None:
            print("No move available.")
        else:
            moves.append(first.move_towards(s_path[1]))
        print("move: ", moves)
    
        return moves
