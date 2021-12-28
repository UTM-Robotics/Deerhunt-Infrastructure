#!/bin/bash
cd .. && gunicorn --chdir server app:app -w 3 --threads 2 --bind 0.0.0.0:5000
