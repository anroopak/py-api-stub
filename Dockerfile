FROM python:2.7

MAINTAINER Roopak A N <anroopak@gmail.com>

RUN pip install flask flask-log-request-id xmltodict

EXPOSE 5000

COPY ./ /code
WORKDIR /code