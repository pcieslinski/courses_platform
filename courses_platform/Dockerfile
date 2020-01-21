###########
# BUILDER #
###########

FROM python:3.7.4-alpine as builder

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY . /usr/src/app

COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


#########
# FINAL #
#########

FROM python:3.7.4-alpine

RUN addgroup -S app && adduser -S app -G app

ENV HOME=/home
ENV APP_HOME=/home/courses_platform/
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

RUN apk update && apk add libpq
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

COPY ./entrypoint.sh $APP_HOME
COPY . $APP_HOME

RUN chmod +x entrypoint.sh

RUN chown -R app:app $APP_HOME

USER app

ENTRYPOINT ["./entrypoint.sh"]
