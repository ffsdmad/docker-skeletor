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

echo Введите CDN_DOMAIN
read CDN_DOMAIN
echo CDN_DOMAIN=$CDN_DOMAIN >>.env

echo Введите CDN_USERNAME
read CDN_USERNAME
echo CDN_USERNAME=$CDN_USERNAME >>.env

echo Введите CDN_PASSWORD
read CDN_PASSWORD
echo CDN_PASSWORD=$CDN_PASSWORD >>.env
