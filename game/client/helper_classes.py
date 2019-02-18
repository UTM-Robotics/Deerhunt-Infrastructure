class Map:
    def __init__(self, map_grid):
        self.grid = map_grid

    def get_tile(self, x, y):
        return self.grid[y][x]


class Units:
    def __init__(self, unit_dict):
        self.units = unit_dict

    def get_unit(self, id):
        return self.units[id]


