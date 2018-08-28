from pyglet.window import key
from directions import Direction

class KeyboardController:
    def __init__(self, key_handler,
               left_key, right_key, up_key, down_key):
        self.key_handler = key_handler
        self.direction_map = {
            left_key:  Direction.LEFT,
            right_key: Direction.RIGHT,
            up_key:    Direction.UP,
            down_key:  Direction.DOWN,
        }
        # Initial direction
        self.direction = Direction.DOWN

    def _get_new_direction(self):
        for key,direction in self.direction_map.items():
            if self.key_handler[key]:
                return direction
        return self.direction

    def tick(self, current_player, other_player_position, other_player_segments):
        self.direction = self._get_new_direction()
        return self.direction
