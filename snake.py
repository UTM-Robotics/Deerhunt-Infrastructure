from random import randrange

from game import Game
from snakeplayer import SnakePlayer
from keyboardcontroller import KeyboardController

class Snake(Game):
    def __init__(self):
        self.player_one = SnakePlayer(KeyboardController(), False)
        self.player_two = SnakePlayer(KeyboardController(), True)
        self.current_food = self.generate_new_food()

    def generate_new_food(self):
        return (randrange(0, 100), randrange(0, 100))

    def handle_food_checks(self):
        one = self.player_one.is_on_food(*self.current_food)
        two = self.player_two.is_on_food(*self.current_food)

        if one and two:
            print('Food collision')
            exit(1)
        elif one and not two:
            self.player_one.size += 1
        elif two and not one:
            self.player_two.size += 1

        self.current_food = self.generate_new_food()

    def does_collide(self, player_one, player_two):
        return (player_one.x, player_one.y) in player_two.segments[:-1]

    def handle_collision_checks(self):
        # TODO: They can hit each other head on
        if does_collide(player_one, player_one):
            print('Player 1 self died')
            exit(1)
        elif does_collide(player_two, player_two):
            print('Player 2 self died')
            exit(1)
        elif does_collide(player_one, player_two):
            print('Player 1 hit player 2')
            exit(1)
        elif does_collide(player_two, player_one):
            print('Player 2 hit player 1')
            exit(1)

    def tick(self):
        self.handle_food_checks()
        self.handle_collision_checks()
        self.player_one.tick()
        self.player_two.tick()
