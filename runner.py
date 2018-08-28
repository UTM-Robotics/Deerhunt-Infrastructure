#!/usr/bin/env python3

import pyglet
from pyglet.window import key

from snake import Snake
from render import SnakeRenderer
from keyboardcontroller import KeyboardController

MAP_WIDTH  = 100
MAP_HEIGHT = 100

clock = 0

window = SnakeRenderer.create_window(MAP_WIDTH, MAP_HEIGHT)
renderer = SnakeRenderer(window)

key_handler = key.KeyStateHandler()
window.push_handlers(key_handler)

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

def update(dt):
    global clock

    if key_handler[key.ESCAPE]:
        pyglet.app.exit()

    clock += dt
    fps_period = 1 / 10

    if clock > fps_period:
        clock -= fps_period
        game.tick()

@window.event
def on_draw():
    window.clear()
    renderer.draw_player_one(game.player_one.get_visible_segments())
    renderer.draw_player_two(game.player_two.get_visible_segments())
    renderer.draw_food(*game.current_food)

if __name__ == '__main__':
    pyglet.clock.schedule(update)
    try:
        pyglet.app.run()
    except Exception:
        pyglet.app.exit()
        raise
