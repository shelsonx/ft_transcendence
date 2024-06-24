GAME_FILE = ./docker-compose.yml
PROJECT_NAME = the_transcendence_journey


up:
	docker-compose -f $(GAME_FILE) --project-name $(PROJECT_NAME) up
stop:
	docker-compose -f $(GAME_FILE) --project-name $(PROJECT_NAME) stop

build:
	docker-compose -f $(GAME_FILE) --project-name $(PROJECT_NAME) up --build

down:
	docker-compose -f $(GAME_FILE) --project-name $(PROJECT_NAME) down --remove-orphans

migrations:
	docker exec -it game-api bash -c "python manage.py makemigrations"

migrate:
	docker exec -t game-api bash -c "python manage.py migrate"

messages:
	docker exec -t game-api bash -c "django-admin makemessages --all"

compilemessages:
	docker exec -t game-api bash -c "django-admin compilemessages"

logs:
	docker logs -f game-api

db-logs:
	docker logs -f game-db

runscript:
	docker exec -it game-api bash -c "python manage.py shell < test.py"

db:
	docker exec -it game-api bash -c "python manage.py shell < utils/seed_base_data.py"

delete-db:
	docker exec -it game-api bash -c "python manage.py shell < utils/delete_objects.py"

shell:
	docker exec -it game-api bash -c "python manage.py shell"

requirements:
	docker exec -t game-api bash -c "pip install -r requirements.txt"

freeze:
	docker exec -t game-api bash -c "pip freeze > requirements.txt"

dump:
	docker exec -it game-api bash -c "python manage.py dumpdata --indent=4 core.GameRules"

exec-api:
	docker exec -it game-api bash

# exec-db:
# 	docker exec -it game-db psql -d game_db -U pong_user

clean:
	docker volume prune

.PHONY: dump
