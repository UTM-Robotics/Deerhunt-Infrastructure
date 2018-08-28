#!/usr/bin/env python3

from pyglet.window import key

from snake import Snake
from render import SnakeRenderer
from keyboardcontroller import KeyboardController

MAP_WIDTH  = 100
MAP_HEIGHT = 100

key_handler = key.KeyStateHandler()
controller_one = KeyboardController(key_handler,
                                    key.LEFT,
                                    key.RIGHT,
                                    key.UP,
                                    key.DOWN)
controller_two = KeyboardController(key_handler,
                                    key.A,
                                    key.D,
                                    key.W,
                                    key.S)

game = Snake(controller_one, controller_two)

renderer = SnakeRenderer(MAP_WIDTH, MAP_HEIGHT, game, key_handler)

@renderer.window.event
def on_draw():
    renderer.window.clear()
    renderer.draw_player_one(renderer.game.player_one.get_visible_segments())
    renderer.draw_player_two(renderer.game.player_two.get_visible_segments())
    renderer.draw_food(*renderer.game.current_food)

if __name__ == '__main__':
    renderer.run()
