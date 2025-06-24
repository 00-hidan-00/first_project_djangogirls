.PHONY: d-dev-start
# Initialize configs and start the development environment from scratch.
d-dev-start:
	@make init-configs-i-dev && \
	make d-run-i-extended


.PHONY: d-run
# Just run
d-run:
	@COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 \
		COMPOSE_PROFILES=full_dev \
		docker-compose up --build


.PHONY: d-run-i-local-dev
# Just run services for local-dev
d-run-i-local-dev:
	@COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 \
		COMPOSE_PROFILES=local_dev \
		docker-compose up --build postgres


.PHONY: d-run-i-extended
# Shutdown previous, run in detached mode, follow logs
d-run-i-extended:
	@COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 COMPOSE_PROFILES=full_dev docker-compose down --timeout 0 && \
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 \
		COMPOSE_PROFILES=full_dev \
		docker-compose up --build --detach && \
	make d-logs-follow


.PHONY: d-stop
# Stop services
d-stop:
	@COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 COMPOSE_PROFILES=full_dev docker-compose down


.PHONY: d-purge-full-dev
# Purge all data related with services in the full_dev profile
d-purge-full-dev:
	@COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 COMPOSE_PROFILES=full_dev docker-compose down --volumes --remove-orphans --rmi local --timeout 0


.PHONY: d-purge-local-dev
# Purge all data related with services in the local_dev profile
d-purge-local-dev:
	@COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 COMPOSE_PROFILES=local_dev docker-compose down --volumes --remove-orphans --rmi local --timeout 0


.PHONY: d-logs-follow
# Follow logs
d-logs-follow:
	@docker-compose logs --follow


.PHONY: migrate
# Apply database migrations
migrate:
	@python manage.py migrate


.PHONY: migrations
# Create new migration
migrations:
	@python manage.py makemigrations


.PHONY: d-migrate
# Apply database migrations inside the Docker container
d-migrate:
	@docker compose exec app python manage.py migrate


.PHONY: d-migrations
# Create new migration files inside the Docker container
d-migrations:
	@docker compose exec app python manage.py makemigrations


.PHONY: init-configs-i-dev
# Make some initialization steps. For example, copy configs.
init-configs-i-dev:
	@cp docker-compose.override.dev.yml docker-compose.override.yml
	@cp .env.example .env


.PHONY: init-dev-i-create-superuser
# Create a Django superuser locally (not in Docker) if it does not exist
init-dev-i-create-superuser:
	@python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')"


.PHONY: d-init-dev-i-create-superuser
# Create a Django superuser inside the Docker container if it does not exist
d-init-dev-i-create-superuser:
	@docker compose exec app python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')"


.PHONY: util-i-kill-by-port
util-i-kill-by-port:
	@sudo lsof -i:8000 -Fp | head -n 1 | sed 's/^p//' | xargs sudo kill
