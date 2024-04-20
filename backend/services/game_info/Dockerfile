FROM python:3.11.4-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app

RUN pip install --upgrade pip
RUN pip install django-bootstrap-v5
RUN pip install -r requirements.txt

COPY . /usr/src/app