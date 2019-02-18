from move import Move

class Map:
    def __init__(self, map_grid):
        self.grid = map_grid

    def get_tile(self, x, y):
        return self.grid[y][x]


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
