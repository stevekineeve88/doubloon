FROM python:3.7-alpine
WORKDIR /code

ARG pg_user
ARG pg_password
ARG pg_host
ARG pg_port
ARG pg_dbname
ARG doubloon_access_id
ARG doubloon_api_key

ENV POSTGRES_USER=$pg_user
ENV POSTGRES_PASS=$pg_password
ENV POSTGRES_HOST=$pg_host
ENV POSTGRES_PORT=$pg_port
ENV POSTGRES_DB=$pg_dbname

ENV DOUBLOON_ACCESS_ID=$doubloon_access_id
ENV DOUBLOON_API_KEY=$doubloon_api_key

ENV FLASK_APP=index.py
ENV FLASK_RUN_HOST=0.0.0.0

COPY ./modules modules
COPY ./routes routes
COPY ./scripts scripts
COPY ./index.py index.py
COPY ./requirements.txt requirements.txt

RUN apk update && apk add python3 \
    gcc \
    libc \
    libffi \
    openssl
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl postgresql && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

CMD ["gunicorn", "--workers=2", "--threads=4", "--worker-class=gthread", "--bind", "0.0.0.0:5000", "index:app"]
EXPOSE 5000