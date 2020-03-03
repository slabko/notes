PYTHONPATH := $(CURDIR)
TAG := $(shell date '+%Y_%m_%d')_$(shell git rev-parse --short HEAD)

run:
	python -m notes.app

check: 
	find . -type d -name '.venv' -prune -o -name '*.py' -print | xargs mypy
	find . -type d -name '.venv' -prune -o -name '*.py' -print | xargs flake8

test:
	coverage run --source ./notes/ -m pytest tests/
	coverage report -m
	coverage html

db:
	python -m notes.bin.make_test_data

docker:
	docker build . -t slabko/${TAG}

docker-run:
	docker-compose build
	docker-compose up -d postgres
	sleep 5
	docker-compose up -d

docker-stop:
	docker-compose stop
	docker-compose rm
