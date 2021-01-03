from move import Move
# from pprint import pprint
from helper_classes import Map, Units

WORKER_TYPE = 'worker'
MELEE_TYPE = 'melee'

class GridPlayer:
    def __init__(self) -> None:
        self.safe_turns = 0

    def tick(self, game_map: Map, your_units: Units, enemy_units: Units,
             resources: int, turns_left: int) -> [Move]:

        print("\n--------RESOURCES: {0} | TURNS LEFT: {1}--------".format(
            resources, turns_left))

        #if turns_left == 100:
        #   do pregrame calcs

        workers = your_units.get_all_unit_of_type(WORKER_TYPE)
        melees = your_units.get_all_unit_of_type(MELEE_TYPE)
        moves = []

        resource_nodes = game_map.find_all_resources()
        asymmetrical_node = resource_nodes[(len(resource_nodes) // 2)]

        print(self.safe_turns)
        print(resource_nodes, asymmetrical_node)

        for unit in workers:
            if unit.can_duplicate(resources, MELEE_TYPE):
                duplicate_move = unit.duplicate('RIGHT', MELEE_TYPE)
                print(duplicate_move)
                moves.append(duplicate_move)
            elif unit.can_mine(game_map):
                moves.append(unit.mine())
            else:
                closest_node = game_map.closest_resources(unit)
                s_path = game_map.bfs(unit.position(), closest_node)
                if s_path:
                    moves.append(unit.move_towards(s_path[1]))

        for unit in melees:
            enemy_list = unit.nearby_enemies_by_distance(enemy_units)
            if enemy_list:
                attack_list = unit.can_attack(enemy_units)
                stun_list = unit.can_stun(enemy_units)
                if attack_list:
                    moves.append(unit.attack(attack_list[0][1]))
                elif stun_list:
                    moves.append(unit.stun(stun_list[0][1]))
                else:
                    closest = enemy_units.units[enemy_list[0][0]]
                    moves.append(unit.move_towards((closest.x, closest.y)))
            else:
                moves.append(unit.move('DOWN'))

        return moves