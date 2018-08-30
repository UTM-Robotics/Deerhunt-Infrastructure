#!/usr/bin/env python3

import socket
import time

s = socket.socket()
host = socket.gethostname()
port = 14447
s.bind((host, port))

s.listen(2)

print('Waiting for first client...')
c1, addr = s.accept()
print('Got connection from', addr)

print('Waiting for second client...')
c2, addr = s.accept()
print('Got connection from', addr)

while True:
    time.sleep(1)
    c1.send(b'client 1')
    print(c1.recv(1024))

    time.sleep(1)
    c2.send(b'client 2')
    print(c2.recv(1024))

c1.close()
c2.close()
