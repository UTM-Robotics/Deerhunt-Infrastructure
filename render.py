import pyglet
from pyglet.window import key

player1 = pyglet.sprite.Sprite(
    img=pyglet.image.load('assets/player1.png'))
player2 = pyglet.sprite.Sprite(
    img=pyglet.image.load('assets/player2.png'))
food = pyglet.sprite.Sprite(
    img=pyglet.image.load('assets/food.png'))

TILE_SIZE     = 10
WINDOW_WIDTH  = 640
WINDOW_HEIGHT = 480
MAP_WIDTH     = int(WINDOW_WIDTH / TILE_SIZE)
MAP_HEIGHT    = int(WINDOW_HEIGHT / TILE_SIZE)

# Hax. This should be nicer :)
directionKey = key.Z

window = pyglet.window.Window(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)

def draw_tile(sprite, x, y):
    sprite.x = x * TILE_SIZE
    sprite.y = (MAP_HEIGHT - y - 1) * TILE_SIZE
    sprite.draw()

def draw_segments(sprite, segments):
    for x,y in segments:
        draw_tile(sprite, x, y)

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.ESCAPE:
        pyglet.app.exit()
    elif symbol in [key.LEFT, key.RIGHT, key.DOWN, key.UP]:
        directionKey = symbol

@window.event
def on_draw():
    window.clear()

    draw_segments(player1, [
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 3),
        (2, 3),
        (3, 3),
        (4, 3),
        (5, 3),
    ])

    draw_segments(player2, [
        (20, 5),
        (20, 6),
        (20, 7),
    ])

clock = 0

def update(dt):
    global clock
    FPS_PERIOD = 1 / 60

    clock += dt

    if clock > FPS_PERIOD:
        clock -= FPS_PERIOD
        # Tick

if __name__ == '__main__':
    pyglet.clock.schedule(update)
    pyglet.app.run()
