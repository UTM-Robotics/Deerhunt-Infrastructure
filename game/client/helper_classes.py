from move import Move
from math import sqrt

class Map:
    def __init__(self, map_grid):
        self.grid = map_grid

    def get_tile(self, x, y):
        return self.grid[y][x]

    def is_wall(self, x, y):
        return self.grid[y][x].lower() == 'x'

    def is_resource(self, x, y):
        return self.grid[y][x].lower() == 'r'

    def closest_resources(self, unit):
        locations = []
        x, y = unit.position()
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.is_resource(self, col, row):
                    locations.append((row, col))

        result = None
        so_far = 999999
        for (r, c) in locations:
            dy = r-y
            dx = c-x
            dist = sqrt(dx**2 + dy**2)
            if dist < so_far:
                result = (r, c)
                so_far = dist

        return result

class Units:
    def __init__(self, units):
        self.units = {}
        for unit in units:
            self.units[str(unit['id'])] = Unit(unit)

    def get_unit(self, id):
        return self.units[id]


class Unit:
    def __init__(self, attr):
        self.id = attr['id']
        self.attr = attr

        self.x = attr['x']
        self.y = attr['y']

    def position(self):
        return self.x, self.y

    def move(self, *directions):
        return Move(self.id, *directions)

    def attack(self, *directions):
        return Move(self.id, *(['ATTACK'] + list(directions)))

    def mine(self):
        return Move(self.id, 'MINE')

