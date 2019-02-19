from move import Move
from pprint import pprint

class GridPlayer:

    def __init__(self):
        self.counter = 0
        pass

    def tick(self, game_map, your_units, enemy_units, resources, turns_left):

        print("\n--------RESOURCES: {0} | TURNS LEFT: {1}--------".format(resources, turns_left))

        moves = []

        #all_units = your_units.get_all_unit_ids()
        #for ids in all_units:
        #    print(ids, " : ", your_units.get_unit(ids).type)


        
        workers = your_units.get_all_unit_of_type('worker')
        melee = your_units.get_all_unit_of_type('melee')

        for unit in workers:
            if unit.can_mine(game_map):
                moves.append(unit.mine())
            else:
                closest_node = game_map.closest_resources(unit)
                s_path = unit.bfs(game_map, closest_node)
                if s_path:
                    moves.append(unit.move_towards(s_path[1]))

        for unit in melee:
            if unit.can_duplicate(resources):
                moves.append(unit.duplicate('LEFT'))
        
        return moves
