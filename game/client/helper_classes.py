from move import Move
from math import sqrt

class Map:
    def __init__(self, map_grid):
        """
        Initialize a new Map.
        """
        self.grid = map_grid

    def get_tile(self, x, y):
        """(int, int) -> str
        Returns the tile found at <x> and <y>.
        
        Preconditions: x >= 0
                       y >= 0
	"""
        return self.grid[y][x]

    def is_wall(self, x, y):
        """(int, int) -> bool
        Return whether the tile at <x> and <y> is a wall.
        
        Preconditions: x >= 0
                       y >= 0	
        """
        return self.grid[y][x].lower() == 'x'

    def is_resource(self, x, y):
        """(int, int) -> bool
        Return whether the tile at <x> and <y> is a resource.
        
        Preconditions: x >= 0
                       y >= 0
        """
        return self.grid[y][x].lower() == 'r'

    def closest_resources(self, unit):
        """(Unit) -> (int, int)
        Returns the location of the closest resource to <unit>.
        """
        locations = []
        x, y = unit.position()
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.is_resource(col, row):
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
        """(___) -> None
        Initialize a new Units.
        """
        self.units = {}
        for unit in units:
            self.units[str(unit['id'])] = Unit(unit)

    def get_unit(self, id):
        """(str) -> Unit
        Returns the Unit with <id>.
        """
        return self.units[id]

class Unit:
    def __init__(self, attr):
        """(___) -> None
        Initialize a new Unit.
        """
        self.id = attr['id']
        self.attr = attr
        
        self.x = attr['x']
        self.y = attr['y']

    def position(self):
        """(None) -> int, int
        Returns the current position of this Unit.
        """
        return self.x, self.y

    def move(self, *directions):
        """(___) -> Move
        Returns a Move for this Unit using the given <*directions>.
        """
        return Move(self.id, *directions)

    def attack(self, *directions):
        """(___) -> Move
        Returns an 'attack' Move for this Unit in the given <*directions>.
        """
        return Move(self.id, 'ATTACK', *directions)

    def mine(self):
        """(None) -> Move
        Returns a 'mine' Move for this Unit.
        """
        return Move(self.id, 'MINE')

    def duplicate(self, direction):
        """(___) -> Move
        Returns a 'duplicate' Move for this Unit in the given <direction>.
        """
        return Move(self.id, 'DUPLICATE', direction)


