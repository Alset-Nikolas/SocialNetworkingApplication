# pull official base image
FROM python:3.10-slim-buster


WORKDIR /social_network_service/src/

ENV VIRTUAL_ENV=env
RUN python3 -m venv $VIRTUAL_ENV


RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .



