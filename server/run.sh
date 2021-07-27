#!/bin/bash

# Check to see if python virtual enviornment is set first.
if [[ -z ${VIRTUAL_ENV} ]]; then
    echo "Python venv not enabled"
    exit
else
    echo "Python venv is enabled. Make sure it is the right one!"
    echo ""
fi

# Flask specific environment variables defined here. Are automatically read in by Flask.
# Read flask configuration doc at: https://flask.palletsprojects.com/en/2.0.x/config/
export FLASK_ENV=development
export TESTING=


# Non Flask environment variables included through python-dotenv

# Running app.py
flask run
