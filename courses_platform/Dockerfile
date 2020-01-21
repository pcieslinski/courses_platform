FROM python:3.7.4-alpine

WORKDIR /home

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY ./requirements.txt /home
RUN pip install -r requirements.txt

COPY . /home

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
