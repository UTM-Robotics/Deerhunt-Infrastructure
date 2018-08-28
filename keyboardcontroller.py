from pyglet.window import key
from directions import Direction

class KeyboardController:
    def __init__(self, key_handler,
               left_key, right_key, up_key, down_key):
        self.key_handler = key_handler
        self.left_key    = left_key
        self.right_key   = right_key
        self.up_key      = up_key
        self.down_key    = down_key
        self.direction   = Direction.DOWN

    def _get_new_direction(self):
        if self.key_handler[self.right_key]:
            return Direction.RIGHT
        elif self.key_handler[self.left_key]:
            return Direction.LEFT
        elif self.key_handler[self.up_key]:
            return Direction.UP
        elif self.key_handler[self.down_key]:
            return Direction.DOWN
        return self.direction

    def tick(self, player):
        self.direction = self._get_new_direction()
        return self.direction
