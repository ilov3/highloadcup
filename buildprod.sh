#!/usr/bin/env bash

python setup.py sdist

docker build -t hlcup .