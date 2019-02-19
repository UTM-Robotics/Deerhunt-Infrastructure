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
            
            enemy_list = unit.nearby_enemies_by_distance(enemy_units)
            if enemy_list:
                attack_list = unit.can_attack(enemy_units)
                #print("attack list: ", attack_list)
                if attack_list:
                    moves.append(unit.attack(attack_list[0][1]))
                else:
                    closest = enemy_units.units[enemy_list[0][0]]
                    moves.append(unit.move_towards( (closest.x, closest.y) ))
            elif unit.can_duplicate(resources):
                    moves.append(unit.duplicate('LEFT'))
            else:
                moves.append(unit.move('DOWN'))
        
        return moves
