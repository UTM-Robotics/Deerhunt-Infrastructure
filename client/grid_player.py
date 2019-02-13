class GridPlayer:

    def __init__(self):
        self.foo = True
        pass

    def tick(self, game_state):
        if self.foo:
            return {'0': ['DOWN']}

        return {}
