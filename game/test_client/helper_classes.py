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
                if self.is_resource(col, row):
                    locations.append((col, row))

        result = None
        so_far = 999999
        for (r, c) in locations:
            dx = r-x
            dy = c-y
            dist = abs(dx) + abs(dy)
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

    def ghetto_move(self, cur, dest):
        if self.x < dest[0]:
            return Move(self.id, 'RIGHT')
        elif self.x > dest[0]:
            return Move(self.id, 'LEFT')
        elif self.y < dest[1]:
            return Move(self.id, 'DOWN')
        elif self.y > dest[1]:
            return Move(self.id, 'UP')

    def attack(self, *directions):
        return Move(self.id, 'ATTACK', *directions)

    def mine(self):
        return Move(self.id, 'MINE')

    def duplicate(self):
        return Move(self.id, 'DUPLICATE', direction)
