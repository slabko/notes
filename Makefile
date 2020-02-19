PYTHONPATH := $(CURDIR)

run:
	python -m notes.app

check: 
	find . -type d -name '.venv' -prune -o -name '*.py' -print | xargs mypy
	find . -type d -name '.venv' -prune -o -name '*.py' -print | xargs flake8

test:
	python -m pytest tests/

db:
	python -m notes.bin.make_test_data
