#!/usr/bin/env bash
python setup.py sdist
docker build -t hlcup .
docker tag hlcup stor.highloadcup.ru/travels/violet_mothi
docker push stor.highloadcup.ru/travels/violet_mothi