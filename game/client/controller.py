import json
import socket

class Controller:
    def tick(self, connection, player):
        raise NotImplementedError('Should have implemented this')

class NetworkedController(Controller):
    def __init__(self, connection, player):
        self.conn = connection
        self.player = player

    def tick(self):
        size = int(self.conn.recv(10).decode())
        response = self.conn.recv(size).decode()

        moves = self.player.tick(json.loads(response))

        data = list(map(lambda x: x.to_tuple(), moves))
        body = json.dumps(data).encode()

        self.conn.sendall('{:10}'.format(len(body)).encode())
        self.conn.sendall(body)

