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
    def __init__(self, unit_dict):
        self.units = {}
        for k, v in unit_dict.items():
            self.units[k] = Unit(v)

    def get_unit(self, id):
        return self.units[id]


class Unit:
    def __init__(self, id, attr):
        self.id = id
        self.attr = attr

        self.x = attr['x']
        self.y = attr['y']

    def position(self):
        return self.x, self.y

    def move(self, *directions):
        return (str(self.id), list(directions))

    def attack(self, *directions):
        return (str(self.id), ['ATTACK'] + list(directions))

    def mine(self):
        return (str(self.id), ['MINE'])

