from directions import Direction


class SnakePlayer:

    def __init__(self, controller, start_point):
        self.size = 1
        self.segments = []
        self.controller = controller
        self.has_died = False

        self.x, self.y = start_point

        self.movement = {
            Direction.UP: self.handle_up,
            Direction.DOWN: self.handle_down,
            Direction.LEFT: self.handle_left,
            Direction.RIGHT: self.handle_right,
        }

    def get_pos_tupple(self):
        return (self.x, self.y)

    def handle_up(self):
        if self.y - 1 < 0:
            self.has_died = True
        else:
            self.y -= 1

    def handle_down(self):
        if self.y + 1 >= 100:
            self.has_died = True
        else:
            self.y += 1

    def handle_left(self):
        if self.x - 1 < 0:
            self.has_died = True
        else:
            self.x -= 1

    def handle_right(self):
        if self.x + 1 >= 100:
            self.has_died = True
        else:
            self.x += 1

    def is_on_food(self, x, y):
        return self.x == x and self.y == y

    def get_visible_segments(self):
        return self.segments[-self.size:]

    def tick(self, game, other_player):
        self.segments.append((self.x, self.y))

        if len(self.segments) > self.size:
            self.segments.pop(0)
        
        move = self.controller.tick(game, self, other_player)

        if move in self.movement:
            self.movement[move]()
        else:
            self.has_died = True
