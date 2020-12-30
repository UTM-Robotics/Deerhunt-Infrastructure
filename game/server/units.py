
MELEE_UNIT = 'melee'
WORKER_UNIT = 'worker'
MELEE_COST = 100
WORKER_COST = 150


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
        self.type = MELEE_UNIT

        super().__init__(x, y)

    def string(self):
        return '"m"'

    def __repr__(self):
        return 'm'

    def is_mining(self):
        return False

    def can_duplicate(self, resources):
        return False

    def is_duplicating(self):
        return False


class WorkerUnit(Unit):
    def __init__(self, x, y):
        self.type = WORKER_UNIT
        self.mining_time = 5
        self.mining_status = 0

        self.duplication_status = 0
        self.stasis_direction = None
        self.duplication_time = 4
        self.duplication_unit = None

        self.melee_cost = MELEE_COST
        self.worker_cost = WORKER_COST

        super().__init__(x, y)

    def string(self):
        return '"w"'

    def __repr__(self):
        return 'w'

    def can_mine(self) -> bool:
        return self.mining_status <= 0

    def is_mining(self) -> bool:
        return self.mining_status > 0

    def start_mining(self):
        self.mining_status = self.mining_time
        return self

    def can_duplicate(self, resouces: int, unit_type: str) -> bool:
        if (unit_type == MELEE_UNIT and resouces >= self.melee_cost) or \
                (unit_type == WORKER_UNIT and resouces >= self.worker_cost):
            return self.duplication_status <= 0
        return False

    def is_duplicating(self) -> bool:
        return self.duplication_status > 0

    def start_duplication(self, direction: str, unit_type: str):
        self.duplication_status = self.duplication_time
        self.stasis_direction = direction
        self.duplication_unit = unit_type
        return self
