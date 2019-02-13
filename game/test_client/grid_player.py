class GridPlayer:

    def __init__(self):
        self.foo = True
        pass

    def tick(self, game_state):
        if self.foo:
            self.foo = False
            return [('0', ['DOWN'])]

        return [('0', ['ATTACK', 'DOWN'])]
