# Pull base image
FROM python:3.10.2-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y gettext && rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN pip install -U pip poetry

ARG APP
ARG UID
ARG GID
ARG USER
ARG HOME

ENV APP $APP

RUN groupadd -r -g $GID $USER
RUN useradd -rm -u $UID -g $GID -d $HOME $USER

USER $USER
# Set work directory
WORKDIR $HOME

COPY ./pyproject.toml poetry.lock gunicorn.conf.py startup-project.sh ./

RUN poetry install

# Copy project
#COPY . .
