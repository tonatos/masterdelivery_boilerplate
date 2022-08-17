#!make
.DEFAULT_GOAL := cq

# Makefile target args
args = $(filter-out $@,$(MAKECMDGOALS))

# Command shortcuts
python = poetry run
flake = poetry run flake8 ./app ./tests
isort = poetry run isort app tests
pytest = ENV=testing poetry run pytest --asyncio-mode=strict
compose = docker-compose


docker-test:
	$(compose) -f docker-compose.test.yml up --build --exit-code-from tests

build:
	$(compose) -f docker-compose.yml build

up:
	$(compose) -f docker-compose.yml up

up-local:
	$(compose) -f docker-compose.yml -f docker-compose.local.yml up -d db redis kafka
	cd ./app && $(python) uvicorn main:app

test:
	$(pytest) --no-cov -s ${args}

test-verbose:
	$(pytest) --no-cov -svvl ${args}

test-cov:
	$(pytest) -vv ${args}

test-watch:
	$(pytest) --no-cov -f -svv --ff ${args}

.PHONY: test-ci
test-ci:
	$(pytest) --junitxml=artefacts/test_report.xml -vv


# Shortcut for code quality (run linting and test with coverage)
.PHONY: cq
cq: test-cov lint

.PHONY: format
format:
	$(isort)

.PHONY: lint
lint:
	$(flake)
	$(isort) --check-only

.PHONY: clean
clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -rf dist *.egg-info
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -f .coverage
	rm -f .coverage.*
	rm -rf artefacts/{htmlcov,test_report.xml}
