# docker-skeletor
Скелет нового Nginx/Gunicor/Postgres/Django проекта в Docker-compositor

Для создания нового проекта неоходимо запустить следующее

bash env.sh  # этот скрипт запросит имя проекта

#  собрать образ
docker-compose build web

#  установить зависимомсти
docker-compose run web poetry install

#  установить создать новый Django проект с именем заданным env.sh
docker-compose run web sh -c 'poetry run django-admin startproject "$APP"'
