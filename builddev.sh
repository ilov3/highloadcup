#!/usr/bin/env bash

python setup.py sdist

docker build -f Dockerfile.dckr -t hlcup-dev .