#!/bin/sh

sleep 2 && python ../p1/client_runner.py $(hostname) $1 > /dev/null &
sleep 3 && python ../p2/client_runner.py $(hostname) $1 > /dev/null &
python server_runner.py $1
