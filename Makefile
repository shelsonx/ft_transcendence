DOCKER_COMPOSE = docker-compose
DOCKER_COMPOSE_FILE = docker-compose.yml
DOCKER_CMD = $(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE)
PROJECT_NAME = the_transcendence_journey

up:
	$(DOCKER_CMD) --project-name $(PROJECT_NAME) up -d

build:
	$(DOCKER_CMD) --project-name $(PROJECT_NAME) up -d --build

stop:
	$(DOCKER_CMD) --project-name $(PROJECT_NAME) stop

down:
	$(DOCKER_CMD) --project-name $(PROJECT_NAME) down --remove-orphans

exec:
	$(DOCKER_CMD) exec $(filter-out $@,$(MAKECMDGOALS)) /bin/sh

logs:
	$(DOCKER_CMD) logs $(filter-out $@,$(MAKECMDGOALS))
