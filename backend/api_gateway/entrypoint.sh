#!/bin/bash

# Collect static files - check if it would be necessary
# python manage.py collectstatic --noinput

python manage.py migrate

exec $@