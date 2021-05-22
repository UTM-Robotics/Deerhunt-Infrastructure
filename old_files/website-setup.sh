#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/../ >/dev/null 2>&1 && pwd )"

sudo mkdir /deerhunt
sudo chown $(whoami): /deerhunt

mkdir /deerhunt/build
mkdir /deerhunt/submissions
mkdir /deerhunt/template
ln -s $DIR/game/server /deerhunt/server
ln -s $DIR/game/client /deerhunt/template/p1
ln -s $DIR/game/client /deerhunt/template/p2
ln -s $DIR/website/submission.dockerfile /deerhunt/template/Dockerfile

