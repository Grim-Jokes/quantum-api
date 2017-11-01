FROM python:3.6-stretch

LABEL project='quantum'

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        bash-completion \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /quantum

WORKDIR /quantum

COPY ./requirements requirements

RUN pip install -r /quantum/requirements/requirements.txt