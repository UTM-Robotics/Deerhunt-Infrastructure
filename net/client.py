#!/usr/bin/env python3

import socket

s = socket.socket()
host = socket.gethostname()
port = 14447

s.connect((host, port))

while True:
    message = s.recv(1024)
    print(message)
    s.send(b'Pong! ' + message)

s.close()
