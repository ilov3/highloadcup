#!/usr/bin/env bash
if [ "$INMEMORY" = "0" ]
then
   /usr/local/bin/python3 -m hlcup.load_util
fi
/usr/local/bin/python3 -m hlcup.app
