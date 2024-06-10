# FROM python:3.9.17-slim-buster
FROM python:alpine3.18

WORKDIR /home/app

COPY requirements.txt .

RUN \
 apk add --no-cache python3 postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps && pip install gunicorn

COPY . .

EXPOSE 5000
CMD gunicorn --bind 0.0.0.0:5000 run:app