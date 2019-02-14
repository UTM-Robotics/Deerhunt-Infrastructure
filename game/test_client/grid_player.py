from move import Move

class GridPlayer:

    def __init__(self):
        self.foo = True
        pass

    def tick(self, game_state):
        if self.foo:
            self.foo = False
            return [Move('0', 'DUPLICATE', 'DOWN')]

        return []
