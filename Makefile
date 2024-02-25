# This Makefile is used to create the Django project and the Django app
DOCKER_COMPOSE = docker-compose
DOCKER_COMPOSE_FILE = docker-compose-auth.yml # This is the docker-compose file # refer to the docker-compose example inside template_config folder
DOCKER_CMD = $(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE)
DOCKER_COMPOSE_SERVICE_NAME = auth-api # This is the service name in the docker-compose file
DOCKER_COMPOSE_PROJECT_NAME = auth_api # This is the app name -> name of the folder
DOCKER_COMPOSE_BUILD_PATH = ./services/auth # This is the path to the Dockerfile

create_api:
	./config_django_project.sh $(DOCKER_COMPOSE_FILE) $(DOCKER_COMPOSE_SERVICE_NAME) $(DOCKER_COMPOSE_PROJECT_NAME) $(DOCKER_COMPOSE_BUILD_PATH)

run_first_api:
	$(DOCKER_CMD) up -d
	$(DOCKER_CMD) run $(DOCKER_COMPOSE_SERVICE_NAME) python manage.py migrate
	$(DOCKER_CMD) run $(DOCKER_COMPOSE_SERVICE_NAME) python manage.py createsuperuser

run_api:
	$(DOCKER_CMD) up -d --build

exec:
	$(DOCKER_CMD) exec $(filter-out $@,$(MAKECMDGOALS)) /bin/sh