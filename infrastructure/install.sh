#!/bin/bash

# Detects which OS script is running on
OS=$(uname)

if [[ ${OS} == 'Linux' ]]; then
   sudo apt install npm
elif [[ ${OS} == 'Darwin' ]]; then
   brew install npm
else
    echo 'Windows currently not supported for development'
fi

# Creating python virtual env and activates it
python3 -m venv venv
source venv/bin/activate

# Installs all required backend python modules to run server.
pip3 install --upgrade -r ./server/requirements.txt

# Installs npm node_modules
pushd deerhunt
npm up
popd