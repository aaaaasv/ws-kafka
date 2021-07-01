FROM python:3

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN apt-get update

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt


COPY . .