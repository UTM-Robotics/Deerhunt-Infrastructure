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
            self.player_one.score += 1
        elif two and not one:
            self.player_two.score += 1

        self.current_food = self.generate_new_food()

    def tick(self):
        self.player_one.tick()
        self.player_two.tick()
