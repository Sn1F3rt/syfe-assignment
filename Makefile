env:
	uv venv

rmenv:
	rm -rf .venv

install:
	uv sync --no-dev

install-dev:
	uv sync --extra dev

export:
	uv export --no-dev --format requirements-txt --no-hashes > requirements.txt

export-dev:
	uv export --format requirements-txt --no-hashes > requirements-dev.txt

test:
	pytest tests/test.py

format:
	ruff check --select I --fix .
	ruff format .

.PHONY: env rmenv install install-dev export export-dev test format
.DEFAULT_GOAL := test
