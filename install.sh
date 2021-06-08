#!/bin/bash

usage() {
   printf "Usage: ./install <options>\n"
   printf "                 -f (installs frontend npm packages)\n"
   printf "                 -b (installs backend pip packages in venv)\n"
   printf "                 -h (print this help menu)\n\n"
   printf "       If no options are provided script just fresh reinstalls everything\n\n"
   exit;
}

install_frontend() {
   pushd deerhunt
   # Deletes existing node modules if exists.
   [ -d "node_modules" ] && rm -rf node_modules
   
   # Installs npm node_modules
   npm install
   popd
}

install_backend() {
   # Deletes existing venv if exists and makes new one.
   [ -d "venv" ] && rm -rf venv
   python3 -m venv venv
   source venv/bin/activate

   # Installs all required backend python modules to run server.
   pip3 install --upgrade -r ./server/requirements.txt
}


while getopts "fbh" o; do
    case "${o}" in
        f)
            FRONTEND=true
            ;;
        b)
            BACKEND=true
            ;;
        h)
            usage
            ;;
        *)
            usage
            ;;
    esac
done

# Detects which OS script is running on
OS=$(uname)

if [[ ${OS} == 'Linux' ]]; then
   sudo apt install npm
elif [[ ${OS} == 'Darwin' ]]; then
   brew install npm
else
    echo 'Windows currently not supported for development'
    exit;
fi

if [ -z "${FRONTEND}" ] && [ -z "${BACKEND}" ]; then
   install_backend
   install_frontend
fi


if [ -n "${BACKEND}" ]; then
   install_backend
fi

if [ -n "${FRONTEND}" ]; then
   install_frontend
fi

printf "\n\n\nInstallation finished. Don't forget to activate venv by doing:\n"
printf "   $ source venv/bin/activate\n\n"