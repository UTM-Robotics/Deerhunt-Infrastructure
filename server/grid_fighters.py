from game import Game
from units import MeleeUnit, RangedUnit


class GridFighters(Game):

    def __init__(self, player_one_connection, player_two_connection, map_file):
        self.grid = map_file

        self.next_id = 0

        self.p1_conn = player_one_connection
        self.p2_conn = player_one_connection

        self.p1_state = {
            'units': {}
        }
        self.p2_state = {
            'units': {}
        }

        self.add_unit(self.p1_state, MeleeUnit(2, 1))
        self.add_unit(self.p2_state, MeleeUnit(2, 3))

    def add_unit(self, player, unit):
        unit.id = self.next_id
        player['units'][self.next_id] = unit
        self.next_id += 1

    def verify_response(self, response, player_state):
        pass

    def make_moves(self, moves, player_state):
        pass

    def tick(self):
        moves = self.p1_conn.tick(self, self.p1_state, self.p2_state)
        if self.verify_response(moves, self.p1_state):
            self.make_moves(moves, self.p1_state)

        moves = self.p2_conn.tick(self, self.p2_state, self.p1_state)
        if self.verify_response(moves, self.p2_state):
            self.make_moves(moves, self.p2_state)
