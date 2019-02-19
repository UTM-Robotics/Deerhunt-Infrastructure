from move import Move

def coordinate_from_direction(x, y, direction):
    # Returns the (x, y) coordinates given a postiion and a direction.
    if direction == 'LEFT':
        return (x-1, y)
    if direction == 'RIGHT':
        return (x+1, y)
    if direction == 'UP':
        return (x, y-1)
    if direction == 'DOWN':
        return (x, y+1)

class Map: # all outputs will be of the form (x, y). i.e., (c, r). 
    def __init__(self, map_grid):
        self.grid = map_grid

    def get_tile(self, x, y):
        return self.grid[y][x]

    def is_wall(self, x, y):
        return self.grid[y][x].lower() == 'x'

    def is_resource(self, x, y):
        return self.grid[y][x].lower() == 'r'

    def find_all_resources(self):
        # Returns the (x, y) coordinates for all resource nodes.
        locations = []
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.is_resource(col, row):
                    locations.append((col, row))
        return locations

    def closest_resources(self, unit):
        # Returns the coordinates for the closest node to unit.
        locations = self.find_all_resources()
        c, r = unit.position()
        result = None
        so_far = 999999
        for (c_2, r_2) in locations:
            dc = c_2-c
            dr = r_2-r
            dist = abs(dc) + abs(dr)
            if dist < so_far:
                result = (c_2, r_2)
                so_far = dist
        return result


class Units:
    def __init__(self, units):
        self.units = {} # a dictionary of unit objects.
        for unit in units:
            self.units[str(unit['id'])] = Unit(unit)

    def get_unit(self, id):
        return self.units[id]

    def get_all_unit_ids(self):
        # Returns the id of all current units.
        all_units_ids = []
        for id in self.units:
            all_units_ids.append(id)
        return all_units_ids
    
    def get_all_unit_of_type(self, type):
        # Returns a list of unit objects of a given type.
        all_units = []
        for id in self.units:
            if self.units[id].type == type:
                all_units.append(self.units[id])
                    
        return all_units

class Unit:
    def __init__(self, attr):
        self.attr = attr
        self.type = attr['type'] # 'worker' or 'melee'.
        self.x = attr['x']
        self.y = attr['y']
        self.id = attr['id']

    def position(self):
        return self.x, self.y

    def direction_to(self, pos):
        # returns the direction from a unit to a certain position (pos[0], pos[1]).
        if self.y < pos[1]:
            return 'DOWN'
        elif self.y > pos[1]:
            return 'UP'
        elif self.x > pos[0]:
            return 'LEFT'
        elif self.x < pos[0]:
            return 'RIGHT'

    def move(self, *directions):
        return Move(self.id, *directions)
 
    def move_towards(self, dest):
        direction = self.direction_to(dest)
        return Move(self.id, direction)

    def nearby_enemies_by_distance(self, enemy_units):
        # returns a sorted list of ids and their distances.
        x = self.x
        y = self.y
        enemies = []
        
        for id in enemy_units.units:
            unit = enemy_units.get_unit(id)
            dist = abs(x - unit.x) + abs(y - unit.y)
            enemies.append((str(unit.id), dist))
            
        enemies.sort(key=lambda tup: tup[1])
        return enemies
    
    def attack(self, *directions):
        return Move(self.id, 'ATTACK', *directions)

    def can_attack(self, enemy_units): # make this a new function called attack_list and make can_attack a directed function at an enemy unit.
        enemies = []
        for id in enemy_units.units:
            unit = enemy_units.get_unit(id)
            direction = self.direction_to((unit.x, unit.y))
            if coordinate_from_direction(self.x, self.y, direction) == (unit.x, unit.y):
                enemies.append((unit, direction))
        return enemies

    def can_duplicate(self, resources):
        if self.type == 'melee' and self.attr['resource_cost'] <= resources and self.attr['duplication_status'] <= 0:
            return True
        else:
            return False
    
    def can_mine(self, game_map):
        if self.type == 'worker' and game_map.is_resource(self.x, self.y) and self.attr['mining_status'] <= 0:
            return True
        else:
            return False

    def mine(self):
        return Move(self.id, 'MINE')

    def duplicate(self, direction):
        return Move(self.id, 'DUPLICATE', direction)

    def bfs(self, game_map, dest):
        # Finds the shortest path from current location to dest. Returns a list where the first entry is current position.
        graph = game_map.grid
        start = (self.x, self.y)
        queue = [[start]]
        vis = set(start)
        if start == dest:
            return None

        while queue:
            path = queue.pop(0)
            node = path[-1]
            r = node[1]
            c = node[0]
            
            if node == dest:
                return path
            for adj in ((c+1, r), (c-1, r), (c, r+1), (c, r-1)):
                if (graph[adj[1]][adj[0]] == ' ' or graph[adj[1]][adj[0]] == 'R') and adj not in vis:
                    queue.append(path + [adj])
                    vis.add(adj)
