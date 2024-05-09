GAME_FILE = ./docker-compose.yml
PROJECT_NAME = transcendence

up:
	docker-compose -f $(GAME_FILE) --project-name $(PROJECT_NAME) up
stop:
	docker-compose -f $(GAME_FILE) --project-name $(PROJECT_NAME) stop

build:
	docker-compose -f $(GAME_FILE) --project-name $(PROJECT_NAME) up --build

down:
	docker-compose -f $(GAME_FILE) --project-name $(PROJECT_NAME) down --remove-orphans

migrations:
	docker exec -t game-api bash -c "python manage.py makemigrations"

migrate:
	docker exec -t game-api bash -c "python manage.py migrate"

logs:
	docker logs -f game-api

db-logs:
	docker logs -f game-db

runscript:
	docker exec -t game-api bash -c "python manage.py shell < test.py"

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

# change this
# exec-db:
# 	docker exec -it game-db psql -d game_db -U pong_user

clean:
	docker volume prune

.PHONY: dump
