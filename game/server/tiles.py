
class Tile:
    pass

class WallTile(Tile):
    def string(self):
        return '"X"'

    def __repr__(self):
        return 'X'

class GroundTile(Tile):
    def string(self):
        return '" "'

    def __repr__(self):
        return ' '

class ResourceTile(Tile):
    def string(self):
        return '"R"'

    def __repr__(self):
        return 'R'
