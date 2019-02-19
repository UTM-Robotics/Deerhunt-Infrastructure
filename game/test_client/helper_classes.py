from move import Move

class Map: # all outputs will be of the form (x, y). i.e., (c, r).
    def __init__(self, map_grid):
        self.grid = map_grid

    def get_tile(self, c, r):
        return self.grid[r][c]

    def is_wall(self, c, r):
        return self.grid[r][c].lower() == 'x'

    def is_resource(self, c, r):
        return self.grid[r][c].lower() == 'r'

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
        self.units = {}
        for unit in units:
            self.units[str(unit['id'])] = Unit(unit)

    def get_unit(self, id):
        return self.units[id]

    def get_all_unit_ids(self, type = 'all'):
        # Returns the id of all current units.
        all_units = []
        if type == 'all':
            for unit in self.units:
                all_units.append(unit)
        else:
            for unit in self.units:
                if unit.type == type:
                    all_units.append(unit)
                    
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

    def move(self, *directions):
        return Move(self.id, *directions)
 
    def move_towards(self, dest):
        r = self.y
        c = self.x
        if r < dest[1]:
            return Move(self.id, 'DOWN')
        elif r > dest[1]:
            return Move(self.id, 'UP')
        elif c > dest[0]:
            return Move(self.id, 'LEFT')
        elif c < dest[0]:
            return Move(self.id, 'RIGHT')

    def nearby_enemies_by_distance(self, their_units):
        # returns a sorted list of ids and their distances.
        x = self.x
        y = self.y
        enemies = []
        
        for unit in their_units:
            dist = abs(x - unit.x) + abs(y - unit.y)
            enemies.append((unit.id, dist))
        return enemies.sort(key=lambda tup: tup[1])
        
    def attack(self, *directions):
        return Move(self.id, 'ATTACK', *directions)

    def can_mine(self, game_map):
        if self.type == 'worker' and game_map.is_resource(self.x, self.y) and self.attr['mining_status'] == 0:
            return True
        else:
            return False

    def mine(self):
        return Move(self.id, 'MINE')

    def duplicate(self):
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
