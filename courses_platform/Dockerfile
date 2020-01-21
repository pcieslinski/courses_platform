FROM python:3.7.4-alpine

WORKDIR /home

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt /home
RUN pip install -r requirements.txt

COPY . /home

RUN ls