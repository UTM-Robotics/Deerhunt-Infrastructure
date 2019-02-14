#!/bin/bash

tmux new -d -s 'deerhunt'
tmux send-keys "server/server_runner.py $1" C-m
tmux new-window
tmux send-keys "sleep 3 && client/client_runner.py $(hostname) $1" C-m
tmux split -h
tmux send-keys "sleep 1 && test_client/client_runner.py $(hostname) $1" C-m
tmux next-window

tmux a
