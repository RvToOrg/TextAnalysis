FROM python:3.8

RUN apt-get update && apt-get install -y \
    pgloader \
    postgresql-client

RUN mkdir -p /var/app
WORKDIR /var/app

COPY ./requirements.txt /tmp/
COPY ./.pgpass /root/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

