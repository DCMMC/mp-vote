#!/bin/bash
export PATH="$HOME/.local/bin:$PATH"
export LD_LIBRARY_PATH=/usr/local/lib
pipenv run python3 ./vote/manage.py makemigrations
pipenv run python3 ./vote/manage.py migrate
nohup pipenv run python3 manage.py process_tasks &
nohup pipenv run python3 ./vote/manage.py runserver 0.0.0.0:8888 &
