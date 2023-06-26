.env:
	bash env.sh

envinstall:
	docker-compose build web
	docker-compose run web poetry install

startproject: .env envinstall
	docker-compose run web sh -c 'poetry run django-admin startproject "$$APP"'

devserve:
	docker-compose run web sh -c 'poetry run "$$APP"/manage.py runserver'
