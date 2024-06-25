#!/bin/bash

# Collect static files - check if it would be necessary
# python manage.py collectstatic --noinput

python manage.py migrate
python manage.py loaddata game_rules
python manage.py loaddata game
python manage.py loaddata game_player
python manage.py loaddata tournament
python manage.py loaddata round
python manage.py loaddata tournament_player

exec $@
