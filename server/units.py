
class Unit:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.id = -1
        self.duplication_status = -1

    def pos_tuple(self):
        return self.x, self.y

    def set_relative_location(self, x, y):
        self.x += x
        self.y += y


class MeleeUnit(Unit):
    def __init__(self, x, y): super().__init__(x, y)

    def __repr__(self):
        return 'm'


class RangedUnit(Unit):
    def __init__(self, x, y): super().__init__(x, y)

    def __repr__(self):
        return 'r'
