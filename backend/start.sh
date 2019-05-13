#!/bin/bash
pipenv run python3 ./vote/manage.py makemigrations
pipenv run python3 ./vote/manage.py migrate
nohup stunnel stunnel/dev_https &
nohup pipenv run python3 ./vote/manage.py process_tasks &
pipenv run python3 ./vote/manage.py runserver 0.0.0.0:8888 --insecure
