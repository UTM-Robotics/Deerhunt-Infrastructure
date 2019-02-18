class Move:
    def __init__(self, unit, *args):
        self.unit = unit
        self.directions = args

    def to_tuple(self):
        return (str(self.unit), self.directions)
