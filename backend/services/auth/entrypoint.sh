#!/bin/bash

# Collect static files - check if it would be necessary
# python manage.py collectstatic --noinput

python manage.py makemigrations
python manage.py migrate

#openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj  "/C=BR/ST=SP/L=SãoPaulo/O=42sp/CN=transcendence-journey.42"

exec $@
