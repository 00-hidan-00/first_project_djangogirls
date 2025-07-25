# ----------------------------------------------------------------------------------------------------------------------
# [local-dev] targets
# ----------------------------------------------------------------------------------------------------------------------

SHELL := /bin/bash

COMPOSE_LOCAL := COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 COMPOSE_PROFILES=local_dev
COMPOSE_FULL := COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 COMPOSE_PROFILES=full_dev

# Run PostgreSQL service in local_dev profile (detached mode omitted for logs)
.PHONY: d-run-local-dev
d-run-local-dev:
	@$(COMPOSE_LOCAL) docker-compose up --build postgres

# Run Django development server locally with activated virtualenv
.PHONY: runserver
runserver:
	@. .venv/bin/activate && python manage.py runserver

# Stop all services in local_dev profile
.PHONY: d-stop-local-dev
d-stop-local-dev:
	@$(COMPOSE_LOCAL) docker-compose down

# Purge all data in local_dev profile (volumes, orphans, images)
.PHONY: d-purge-local-dev
d-purge-local-dev:
	@$(COMPOSE_LOCAL) docker-compose down --volumes --remove-orphans --rmi local --timeout 0

# Apply Django migrations locally (outside Docker)
.PHONY: migrate
migrate:
	@python manage.py migrate

# Create new Django migration files locally
.PHONY: migrations
migrations:
	@python manage.py makemigrations

# Create Django superuser locally if it doesn't exist
.PHONY: init-dev-create-superuser
init-dev-create-superuser:
	@python manage.py shell -c "import os; from django.contrib.auth import get_user_model; User = get_user_model(); username = os.environ.get('superuser_username', 'admin'); User.objects.filter(username=username).exists() or User.objects.create_superuser(username, 'admin@example.com', 'admin')"

# Initialize configs for local development (copy overrides and env files)
.PHONY: init-configs-local-dev
init-configs-local-dev:
	@cp docker-compose.override.dev.yml docker-compose.override.yml
	@cp .env.example .env

# Kill process occupying port 8000 (if any)
.PHONY: util-kill-port-8000
util-kill-port-8000:
	@pid=$$(sudo lsof -i:8000 -t); if [ -n "$$pid" ]; then sudo kill $$pid; fi

# ----------------------------------------------------------------------------------------------------------------------
# [full_dev] targets
# ----------------------------------------------------------------------------------------------------------------------

# Initialize configs and start full_dev environment from scratch
.PHONY: d-dev-start-full-dev
d-dev-start-full-dev: init-configs-local-dev d-run-extended-full-dev

# Run all services with full_dev profile
.PHONY: d-run-full-dev
d-run-full-dev:
	@$(COMPOSE_FULL) docker-compose up --build

# Stop all services and restart in detached mode with logs followed (full_dev)
.PHONY: d-run-extended-full-dev
d-run-extended-full-dev:
	@$(COMPOSE_FULL) docker-compose down --timeout 0 && \
	$(COMPOSE_FULL) docker-compose up --build --detach && \
	make d-logs-follow-full_dev

# Stop all services in full_dev profile
.PHONY: d-stop-full-dev
d-stop-full-dev:
	@$(COMPOSE_FULL) docker-compose down

# Purge all data in full_dev profile (volumes, orphans, images)
.PHONY: d-purge-full-dev
d-purge-full-dev:
	@$(COMPOSE_FULL) docker-compose down --volumes --remove-orphans --rmi local --timeout 0

# Follow logs of docker-compose services
.PHONY: d-logs-follow-full_dev
d-logs-follow-full_dev:
	@COMPOSE_PROFILES=full_dev docker-compose logs --follow

# Apply Django migrations inside the app container
.PHONY: d-migrate
d-migrate:
	@COMPOSE_PROFILES=full_dev docker compose exec app python manage.py migrate

# Create new Django migrations inside the app container
.PHONY: d-migrations
d-migrations:
	@COMPOSE_PROFILES=full_dev docker compose exec app python manage.py makemigrations

# Create Django superuser inside the app container if not exists
.PHONY: d-init-dev-create-superuser
d-init-dev-create-superuser:
	@COMPOSE_PROFILES=full_dev docker compose exec app python manage.py shell -c "import os; from django.contrib.auth import get_user_model; User = get_user_model(); username = os.environ.get('superuser_username', 'admin'); User.objects.filter(username=username).exists() or User.objects.create_superuser(username, 'admin@example.com', 'admin')"

# ----------------------------------------------------------------------------------------------------------------------
# [pre commit commands] targets
# ----------------------------------------------------------------------------------------------------------------------

.PHONY: pre-commit-init
pre-commit-init:
	@pip install --upgrade pip && \
	pip install --requirement requirements.txt && \
	pre-commit install

.PHONY: pre-commit-run-all
pre-commit-run-all:
	@pre-commit run --all-files

.PHONY: pre-commit-clean
pre-commit-clean:
	@pre-commit clean

# ----------------------------------------------------------------------------------------------------------------------
# [management commands] targets
# ----------------------------------------------------------------------------------------------------------------------

AMOUNT_POSTS ?= 10
AMOUNT_COMMENTS ?= 5

.PHONY: dev-generate-posts-comments
dev-generate-posts-comments:
	@python manage.py generate_posts_comments --amount_posts $(AMOUNT_POSTS) --amount_comments $(AMOUNT_COMMENTS)

.PHONY: dev-generate-posts
dev-generate-posts:
	@python manage.py generate_posts --amount $(AMOUNT_POSTS)

.PHONY: dev-delete-posts
dev-delete-posts:
	@python manage.py remove_posts --force

.PHONY: dev-generate-comments
dev-generate-comments:
	@python manage.py generate_comments --amount $(AMOUNT_COMMENTS)

.PHONY: dev-delete-comments
dev-delete-comments:
	@python manage.py remove_comments --force