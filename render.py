import pyglet
from pyglet.window import key

TILE_SIZE = 10

class SnakeRenderer:
    def __init__(self, window):
        self.window = window
        self.map_width  = int(window.width / TILE_SIZE)
        self.map_height = int(window.height / TILE_SIZE)

        self.player_one_sprite = pyglet.sprite.Sprite(
            img=pyglet.image.load('assets/player1.png'))
        self.player_two_sprite = pyglet.sprite.Sprite(
            img=pyglet.image.load('assets/player2.png'))
        self.food_sprite = pyglet.sprite.Sprite(
            img=pyglet.image.load('assets/food.png'))

    def create_window(width, height):
        return pyglet.window.Window(width=TILE_SIZE*width, height=TILE_SIZE*height)

    def _draw_tile(self, sprite, x, y):
        sprite.x = x * TILE_SIZE
        sprite.y = (self.map_height - y - 1) * TILE_SIZE
        sprite.draw()

    def _draw_segments(self, sprite, segments):
        for x,y in segments:
            self._draw_tile(sprite, x, y)

    def draw_food(self, x, y):
        self._draw_tile(self.food_sprite, x, y)

    def draw_player_one(self, segments):
        self._draw_segments(self.player_one_sprite, segments)

    def draw_player_two(self, segments):
        self._draw_segments(self.player_two_sprite, segments)

