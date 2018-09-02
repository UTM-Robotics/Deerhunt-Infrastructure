from random import randrange

from game import Game
from snakeplayer import SnakePlayer
from controller import Controller

class Snake(Game):
    def __init__(self, player_one_controller: Controller,
               player_two_controller: Controller,
               map_width: int, map_height: int):
        self.map_width = map_width
        self.map_height = map_height

        player_one_pos_x = int(map_width * 1/3)
        player_two_pos_x = int(map_width * 2/3)
        player_pos_y     = int(map_height / 2)

        player_one_pos = (player_one_pos_x, player_pos_y)
        player_two_pos = (player_two_pos_x, player_pos_y)

        self.player_one = SnakePlayer(player_one_controller,
                                      player_one_pos)
        self.player_two = SnakePlayer(player_two_controller,
                                      player_two_pos)
        self.current_food = self.generate_new_food()

    def generate_new_food(self):
        return (randrange(0, self.map_width),
                randrange(0, self.map_height))

    def handle_food_checks(self):
        one = self.player_one.is_on_food(*self.current_food)
        two = self.player_two.is_on_food(*self.current_food)

        if one and two:
            self.player_one.has_died = True
            self.player_two.has_died = True
            self.current_food = self.generate_new_food()
        elif one and not two:
            self.player_one.size += 1
            self.current_food = self.generate_new_food()
        elif two and not one:
            self.player_two.size += 1
            self.current_food = self.generate_new_food()

    def does_collide(self, player_one, player_two):
        return (player_one.x, player_one.y) in player_two.segments[:-1]

    def handle_collision_checks(self):
        if self.player_one.x == self.player_two.x and self.player_one.y == self.player_two.y:
            print('Head on collision')
            self.player_one.has_died = True
            self.player_two.has_died = True
        elif self.does_collide(self.player_one, self.player_one):
            print('Player 1 self died')
            self.player_one.has_died = True
        elif self.does_collide(self.player_two, self.player_two):
            print('Player 2 self died')
            self.player_two.has_died = True
        elif self.does_collide(self.player_one, self.player_two):
            print('Player 1 hit player 2')
            self.player_one.has_died = True
        elif self.does_collide(self.player_two, self.player_one):
            print('Player 2 hit player 1')
            self.player_two.has_died = True

    def player_has_died(self):
        return self.player_one.has_died or self.player_two.has_died

    def noop(self):
        pass

    def tick(self):
        self.handle_food_checks()
        self.handle_collision_checks()

        if self.player_has_died():
            self.tick = self.noop

        self.player_one.tick(self, self.player_two)
        self.player_two.tick(self, self.player_one)
