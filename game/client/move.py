class Move:
    def __init__(self, unit: int, *args: (str)):
        self.unit = unit
        self.directions = args

    def to_tuple(self) -> (int, (str)):
        return (self.unit, self.directions)
