
class Unit:
    def __init__(self, x, y, duplication_time):
        self.x = x
        self.y = y
        self.id = -1
        self.duplication_time = duplication_time
        self.duplication_status = 0
        self.stasis_direction = None

    def pos_tuple(self):
        return self.x, self.y

    def set_relative_location(self, x, y):
        self.x += x
        self.y += y

    def can_duplicate(self):
        return self.duplication_status <= 0

    def is_duplicating(self):
        return self.duplication_status > 0

    def start_duplication(self, direction):
        self.duplication_status = self.duplication_time
        self.stasis_direction = direction
        return self

class MeleeUnit(Unit):
    def __init__(self, x, y): super().__init__(x, y, 4)

    def __repr__(self):
        return 'm'


class RangedUnit(Unit):
    def __init__(self, x, y): super().__init__(x, y, 8)

    def __repr__(self):
        return 'r'
