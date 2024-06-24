FROM python:3.11.4-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /api

RUN apt-get update && \
    apt-get install -y gettext && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /api

# RUN django-admin makemessages --all
# RUN django-admin compilemessages

RUN chmod +x ./entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]
CMD ["python", "manage.py", "runserver_plus", "--key-file", "selftest-key", "--cert-file", "selftest-cert", "0.0.0.0:8000"]
