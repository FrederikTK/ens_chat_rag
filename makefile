DOCKER_COMPOSE := docker compose

.PHONY: build up down logs test lint index-files delete-vectors test-real index-stats operation-status chat

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

index-files:
	$(DOCKER_COMPOSE) run --rm indexer python -m src.data_processing.index_processed_files $(if $(LIMIT),--limit $(LIMIT),)
#make index-files | make index-files LIMIT=50

delete-vectors:
	$(DOCKER_COMPOSE) run --rm delete_vectors

test-real:
	$(DOCKER_COMPOSE) run --rm -e PYTHONPATH=/app app python tests/real_content_test.py

operation-status:
	$(DOCKER_COMPOSE) run --rm app python -c "from src.utils.operation_lock import OperationLock; print(f'Current operation: {OperationLock().get_current_operation() or "None"}')"

chat:
	$(DOCKER_COMPOSE) run --rm -e PYTHONPATH=/app app python src/chat_interface.py
