from directions import Direction


class SnakePlayer:
    
    def __init__(self, controller, second_player=False):
        self.size = 1
        self.segments = []
        self.controller = controller

        self.x = 74 if second_player else 24
        self.y = 74 if second_player else 24

        self.movement = {
            Direction.UP : self.handle_up,
            Direction.DOWN : self.handle_down,
            Direction.LEFT : self.handle_left,
            Direction.RIGHT : self.handle_right,
        }

    def handle_up(self):
        if self.y - 1 < 0: exit(1)
        self.y -= 1

    def handle_down(self):
        if self.y + 1 >= 100: exit(1)
        self.y += 1

    def handle_left(self):
        if self.x - 1 < 0: exit(1)
        self.x -= 1

    def handle_right(self):
        if self.x + 1 >= 100: exit(1)
        self.x += 1

    def is_on_food(self, x, y):
        return self.x == x and self.y == y

    def tick(self):
        self.segments.append((self.x, self.y))
        move = self.controller.tick(self)

        if move in self.movement:
            self.movement[move]()
        else:
            print('Invalid move')
            exit(1)
