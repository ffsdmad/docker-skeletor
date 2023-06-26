#!/bin/bash

PORT=8888
echo APP_UID=`id -u` > .env
echo APP_GID=`id -g` >> .env

echo Введите название приложения

read APP

echo APP=$APP >> .env
echo APP_USER=$APP >> .env
echo APP_HOME=/home/$APP >> .env
echo PORT=$PORT >> .env

echo DEBUG=True >> .env

echo ALLOWED_HOSTS=0.0.0.0 >> .env
echo CSRF_TRUSTED_ORIGINS=http://0.0.0.0:$PORT >> .env


