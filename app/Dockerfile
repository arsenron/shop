FROM python:3.10-slim as builder

ENV POETRY_VERSION=1.1.13

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN mkdir /app/src && touch /app/src/__init__.py

RUN POETRY_VIRTUALENVS_CREATE=false poetry install --no-interaction --no-ansi

RUN rm -r /app/src

COPY . /app
