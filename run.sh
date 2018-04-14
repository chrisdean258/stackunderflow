#!/bin/bash
export FLASK_APP=app.py
export FLASK_DEBUG=1
#export LANG=C.UTF-8
#export LC_ALL=C.UTF-8

pkill -9 flask
pkill -9 python
pkill -9 python3

if [ $# -eq 0 ]; then
	flask run --host=0.0.0.0
else
	flask run --host=0.0.0.0 &>/dev/null &
fi
