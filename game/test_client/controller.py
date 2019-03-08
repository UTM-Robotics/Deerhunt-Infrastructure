import json
from helper_classes import Map, Units
from move import Move
from grid_player import GridPlayer
from socket import socket


class SocketClosed(Exception):
    pass


class Controller:
    def tick(self, connection: socket, player: GridPlayer):
        raise NotImplementedError('Should have implemented this')


class NetworkedController(Controller):
    def __init__(self, connection: socket, player: GridPlayer):
        self.conn = connection
        self.player = player

    def safe_recv(self, size: int) -> bytes:
        tmp = self.conn.recv(size)
        if tmp == b'':
            raise SocketClosed()
        return tmp

    def tick(self) -> None:
        try:
            size = int(self.safe_recv(10).decode())
            response = self.safe_recv(size).decode()

            js = json.loads(response)
            moves = self.player.tick(Map(js['map']),
                                     Units(js['my_units']),
                                     Units(js['their_units']),
                                     js['my_resources'],
                                     js['turns_left'])
            data = []
            for move in moves:
                if isinstance(move, Move):
                    data.append(move.to_tuple())
                else:
                    print('Expected type Move but got {}'.format(type(move)))

            body = json.dumps(data).encode()

            self.conn.sendall('{:10}'.format(len(body)).encode())
            self.conn.sendall(body)

            return True

        except SocketClosed:
            return False
