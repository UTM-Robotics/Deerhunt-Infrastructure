#!/usr/bin/env python3

import pyglet

from snake import Snake
from render import SnakeRenderer

game = Snake()
clock = 0

WINDOW_WIDTH  = 640
WINDOW_HEIGHT = 480
window = pyglet.window.Window(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
renderer = SnakeRenderer(window)

def update(dt):
    global clock

    clock += dt
    FPS_PERIOD = 1 / 60

    if clock > FPS_PERIOD:
        clock -= FPS_PERIOD
        game.tick()


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.ESCAPE:
        pyglet.app.exit()
    elif symbol in [key.LEFT, key.RIGHT, key.DOWN, key.UP]:
        print('Pressed an arrow!!!!111!!!')

@window.event
def on_draw():
    window.clear()
    renderer.draw_player_one(game.player_one.segments)
    renderer.draw_player_two(game.player_two.segments)
    renderer.draw_food(*game.current_food)

if __name__ == '__main__':
    pyglet.clock.schedule(update)
    try:
        pyglet.app.run()
    except Exception:
        pyglet.app.exit()
