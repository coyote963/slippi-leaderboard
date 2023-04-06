# Slippi Leaderboard

It is a leaderboard for displaying slippi rankings. To be added to the leaderboard, users input their slippi tags into the website. There is an automatic job that runs every 12 hours to get updated slippi ratings from approved users. Admins approve slippi accounts via the built-in Django admin panel.

#### Install & Enter VirtualEnv

`poetry install`
`pip install hypercorn`
`poetry shell`

#### Django commands

`python manage.py runserver_plus`

Run development server

`export DJANGO_SECRET_KEY=$(python manage.py generate_password --length 50)`

Generate a secret key

`python manage.py makemigrations`

Run with hypercorn:

`hypercorn slippi_leaderboard.asgi:application`

Make some changes to the database? Generate the necessary migrations

`python manage.py migrate`

Commit the generated migrations to the database

`python manage.py test`

Run test cases. Requires that you installed dev dependencies

`python manage.py update_accounts`

Grab updated slippi data for approved accounts
