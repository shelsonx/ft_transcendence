# syntax=docker/dockerfile:1
FROM python:3.11.4-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --upgrade pip
RUN pip install django-bootstrap-v5
RUN pip install -r requirements.txt

COPY . /code/

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000"]
