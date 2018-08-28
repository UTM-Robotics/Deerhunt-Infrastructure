#!/usr/bin/env python3

import pyglet

from snake import Snake
from render import SnakeRenderer

game = Snake()
clock = 0

window = SnakeRenderer.create_properly_sized_window()
renderer = SnakeRenderer(window)

def update(dt):
    global clock

    clock += dt
    fps_period = 1 / 60

    if clock > fps_period:
        clock -= fps_period
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
