FROM python:3.6-stretch

LABEL project='quantum'

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        bash-completion \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update -y
RUN apt-get install qt5-default libqt5webkit5-dev build-essential \
                  python-lxml python-pip xvfb -y

RUN mkdir /quantum

WORKDIR /quantum

COPY ./requirements requirements

RUN pip install -r /quantum/requirements/requirements.txt
