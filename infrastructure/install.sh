#!/usr/bin/env bash

# must have these pre installed: 
# - python3 pip
# - npm

python3 -m venv venv
. venv/bin/activate

pip3 install --upgrade -r ./requirements.txt