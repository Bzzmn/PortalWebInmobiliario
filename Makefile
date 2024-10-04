install: 
	#install commands
	python -m pip install --upgrade pip &&\
	python -m pip install -r requirements.txt
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
	docker run --env-file .env --name inmobiliario -p 127.0.0.1:8889:8889 inmobiliario

all: install format lint test build run