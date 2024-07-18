DOCKER_COMPOSE := docker compose

.PHONY: build up down logs test lint test-real

build:
	$(DOCKER_COMPOSE) build

up:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down

logs:
	$(DOCKER_COMPOSE) logs

test:
	$(DOCKER_COMPOSE) run --rm app ./test_endpoints.sh

lint:
	$(DOCKER_COMPOSE) run --rm app flake8 src/ tests/

test-real:
	$(DOCKER_COMPOSE) run --rm -e PYTHONPATH=/app app python tests/real_content_test.py