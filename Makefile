.PHONY: install_prehook lint compress rebuild-db
.DEFAULT_GOAL := lint

install_prehook:
	pre-commit install

lint:
	black --check --diff .
	flake8

format: 
	black .

compress:
	./scripts/compress.sh

rebuild-db:
	./scripts/rebuild-db.sh
