#!/bin/bash

export SECRET_KEY=$(python manage.py generate_password --length 50)

python manage.py migrate

python manage.py update_accounts

hypercorn --bind '0.0.0.0:8000' slippi_leaderboard.asgi:application