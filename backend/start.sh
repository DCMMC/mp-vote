#!/bin/bash
pipenv run python3 ./vote/manage.py makemigrations
pipenv run python3 ./vote/manage.py migrate
nohup pipenv run python3 manage.py process_tasks &
pipenv run python3 ./vote/manage.py runserver 0.0.0.0:8080
