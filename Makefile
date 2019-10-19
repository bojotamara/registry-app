.PHONY: install_prehook lint

install_prehook:
	pre-commit install

lint:
	black --check --diff .
	flake8

format: black .
