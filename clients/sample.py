#!/usr/bin/env python3

import argparse
import json
import socket

parser = argparse.ArgumentParser()
parser.add_argument('host', type=str,
                    help='The host to connect to')
parser.add_argument('port', type=int,
                    help='The port to listen on')
args = parser.parse_args()

sock = socket.socket()
sock.connect((args.host, args.port))

while True:
    message = sock.recv(1024)
    data = json.loads(message)
    print(data)
    sock.send('down'.encode('utf-8'))

sock.close()
