# Load environment variables from .env file
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

PORT ?= 8000  # Default port if not set in .env

install: 
	#install commands
	uv add -r requirements.txt

format: 
	#format code
	python -m black *.py webPages/*.py inmobiliario/*.py

lint:
	#flake8 or #pylint
	python -m pylint --load-plugins pylint_django --django-settings-module=inmobiliario.settings --disable=R,C,W1203 *.py webPages/*.py inmobiliario/*.py --ignore=migrations

test:
	#test
	python -m pytest -vv --cov=webPages

build:
	#build container
	docker build -t inmobiliario .

run-local:
	#run check if container exists and if so remove it then run container
	@if [ $$(docker ps -a -q -f name=inmobiliario) ]; then \
	docker rm -f inmobiliario; \
	fi
	docker run --env-file .env --name inmobiliario -p 0.0.0.0:$(PORT):$(PORT) inmobiliario

load-fixtures:
	#load initial data
	python manage.py flush --no-input &&\
	python manage.py loaddata webPages/fixtures/usuarios.json &&\
	python manage.py loaddata webPages/fixtures/tipos_inmueble.json &&\
	python manage.py loaddata webPages/fixtures/regiones_comunas.json &&\
	python manage.py loaddata webPages/fixtures/inmuebles_adapted.json

collect-static:
	#collect static files
	python manage.py collectstatic --noinput

migrate:
	#run migrations
	python manage.py makemigrations &&\
	python manage.py migrate

dev: install migrate load-fixtures collect-static
	#run development server
	python manage.py runserver 0.0.0.0:$(PORT)

all: install format lint test build run