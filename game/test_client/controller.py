import json
import socket
from helper_classes import *

class SocketClosed(Exception):
    pass

class Controller:
    def tick(self, connection, player):
        raise NotImplementedError('Should have implemented this')

class NetworkedController(Controller):
    def __init__(self, connection, player):
        self.conn = connection
        self.player = player

    def safe_recv(self, size):
        tmp = self.conn.recv(size)
        if tmp == b'':
            raise SocketClosed()
        return tmp

    def tick(self):
        try:
            size = int(self.safe_recv(10).decode())
            response = self.safe_recv(size).decode()

            js = json.loads(response)
            moves = self.player.tick(Map(js['map']), 
                    Units(js['my_units']),
                    Units(js['their_units']),
                    js['my_resources'],
                    js['turns_left'])

            data = list(map(lambda x: x.to_tuple(), moves))
            body = json.dumps(data).encode()

            self.conn.sendall('{:10}'.format(len(body)).encode())
            self.conn.sendall(body)

            return True

        except SocketClosed:
            return False

