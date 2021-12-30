#!/bin/bash
cd .. && gunicorn --chdir server app:app -w 5 --threads 2 --bind 0.0.0.0:5000 --log-level=debug --capture-output
