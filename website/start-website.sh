#!/bin/bash

source /usr/local/bin/virtualenvwrapper.sh
workon deerhunt-site
npm run production
