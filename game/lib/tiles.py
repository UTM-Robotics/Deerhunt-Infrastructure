
class Tile:
    pass

class WallTile(Tile):
    def __repr__(self):
        return 'X'

class GroundTile(Tile):
    def __repr__(self):
        return ' '

class ResourceTile(Tile):
    def __repr__(self):
        return 'R'
