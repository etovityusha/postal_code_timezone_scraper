FROM python:3.9

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR .

RUN apt-get -y update
RUN apt-get -y upgrade

RUN apt-get install -y chromium
RUN apt-get install -y chromium-driver

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
