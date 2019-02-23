
class Unit:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.id = -1

    def pos_tuple(self):
        return self.x, self.y

    def set_relative_location(self, all_units, x, y):
        nx = self.x + x
        ny = self.y + y

        if '{},{}'.format(nx, ny) not in all_units:
            self.x = nx
            self.y = ny

    def can_duplicate(self, resouces):
        raise NotImplemented()

    def is_duplicating(self):
        raise NotImplemented()


class MeleeUnit(Unit):
    def __init__(self, x, y):
        self.type = "melee"
        self.duplication_time = 4
        self.resource_cost = 100

        self.duplication_status = 0
        self.stasis_direction = None

        super().__init__(x, y)

    def string(self):
        return '"m"'

    def __repr__(self):
        return 'm'

    def can_duplicate(self, resouces):
        return self.duplication_status <= 0

    def is_duplicating(self):
        return self.duplication_status > 0

    def start_duplication(self, direction):
        self.duplication_status = self.duplication_time
        self.stasis_direction = direction
        return self


class WorkerUnit(Unit):
    def __init__(self, x, y):
        self.type = "worker"
        self.mining_time = 5
        self.mining_status = 0

        super().__init__(x, y)

    def string(self):
        return '"w"'

    def __repr__(self):
        return 'w'

    def can_mine(self):
        return self.mining_status <= 0

    def is_mining(self):
        return self.mining_status > 0

    def start_mining(self):
        self.mining_status = self.mining_time
        return self

    def can_duplicate(self, resources):
        return False

    def is_duplicating(self):
        return False
