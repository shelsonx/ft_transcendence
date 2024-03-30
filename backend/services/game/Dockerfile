FROM python:3.11.4-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /api

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . ./
RUN chmod +x ./entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]

