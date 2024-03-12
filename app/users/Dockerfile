FROM python:3.11.4-slim-buster

WORKDIR /users

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY . /users

RUN pip install -r requirements.txt

