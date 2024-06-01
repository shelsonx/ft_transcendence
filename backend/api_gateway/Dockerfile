# syntax=docker/dockerfile:1
FROM python:3.11.4-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

RUN chmod +x ./entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]

CMD ["python", "manage.py", "runserver_plus", "--key-file", "selftest-key", "--cert-file", "selftest-cert", "0.0.0.0:80"]
