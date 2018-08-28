from directions import Direction


class SnakePlayer:

    def __init__(self, controller, second_player=False):
        self.size = 1
        self.segments = []
        self.controller = controller
        self.has_died = False

        self.x = 20 if second_player else 10
        self.y = 20 if second_player else 10

        self.movement = {
            Direction.UP : self.handle_up,
            Direction.DOWN : self.handle_down,
            Direction.LEFT : self.handle_left,
            Direction.RIGHT : self.handle_right,
        }

    def handle_up(self):
        if self.y - 1 < 0:
            has_died = True
        else:
            self.y -= 1

    def handle_down(self):
        if self.y + 1 >= 100:
            has_died = True
        else:
            self.y += 1

    def handle_left(self):
        if self.x - 1 < 0:
            has_died = True
        else:
            self.x -= 1

    def handle_right(self):
        if self.x + 1 >= 100:
            has_died = True
        else:
            self.x += 1

    def is_on_food(self, x, y):
        return self.x == x and self.y == y

    def get_visible_segments(self):
        return self.segments[-self.size:]

    def tick(self):
        self.segments.append((self.x, self.y))
        move = self.controller.tick(self)

        if move in self.movement:
            self.movement[move]()
        else:
            self.has_died = True
