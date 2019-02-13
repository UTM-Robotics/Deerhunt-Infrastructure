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
        response = self.conn.recv(1024)

        move = self.player.tick(json.loads(response.decode()))

        self.conn.send(json.dumps(move).encode())

