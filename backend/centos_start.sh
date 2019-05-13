#!/bin/bash
export PATH="$HOME/.local/bin:$PATH"
export LD_LIBRARY_PATH=/usr/local/lib
kill $(ps aux | grep -E 'python.*vote.*' | awk '{print $2}')
kill $(ps aux | grep -E 'stunnel.*dev_https.*' | awk '{print $2}')
pipenv run python3 ./vote/manage.py makemigrations
pipenv run python3 ./vote/manage.py migrate
nohup stunnel stunnel/dev_https &
nohup pipenv run python3 ./vote/manage.py process_tasks &
nohup pipenv run python3 ./vote/manage.py runserver 0.0.0.0:8888 &
