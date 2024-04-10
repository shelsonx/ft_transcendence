#!/usr/bin/bash
# VARIABLES
DOCKER_COMPOSE_FILE=$1 # This is the docker-compose file
DOCKER_COMPOSE_SERVICE_NAME=$2 # This is the service name in the docker-compose file
DOCKER_COMPOSE_PROJECT_NAME=$3 # This is the app name -> name of the folder
DOCKER_COMPOSE_BUILD_PATH=$4 # This is the path to the Dockerfile
TEMPLATE_DOCKERFILE="./template_config" # This is the path to the Dockerfile

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

check_var() {
    if [ -z "$1" ]; then
        echo "Please provide the $2"
        exit 1
    fi
}

check_var "$DOCKER_COMPOSE_FILE" "docker-compose file"
check_var "$DOCKER_COMPOSE_SERVICE_NAME" "service name in the docker-compose file"
check_var "$DOCKER_COMPOSE_PROJECT_NAME" "app name -> name of the folder"
check_var "$DOCKER_COMPOSE_BUILD_PATH" "path to the Dockerfile"

if [ -d "$DOCKER_COMPOSE_BUILD_PATH"/$DOCKER_COMPOSE_PROJECT_NAME ]; then
    echo "The path $DOCKER_COMPOSE_BUILD_PATH/$DOCKER_COMPOSE_PROJECT_NAME already exists"
    exit 1
fi

if [ -d "$DOCKER_COMPOSE_BUILD_PATH" ]; then
    echo "The path $DOCKER_COMPOSE_BUILD_PATH already exists"
else
    echo "$BLUE""The path $DOCKER_COMPOSE_BUILD_PATH does not exist, creating now$NC"
    mkdir -p "$DOCKER_COMPOSE_BUILD_PATH"
fi

echo "$GREEN""Copying the Dockerfile and requirements.txt to $DOCKER_COMPOSE_BUILD_PATH$NC"
cp ./template_config/Dockerfile ./template_config/requirements.txt $DOCKER_COMPOSE_BUILD_PATH

echo "Creating $DOCKER_COMPOSE_SERVICE_NAME Django project"
sudo docker-compose -f "$DOCKER_COMPOSE_FILE" run "$DOCKER_COMPOSE_SERVICE_NAME" django-admin startproject "$DOCKER_COMPOSE_PROJECT_NAME" . 
sudo chown -R $USER:$USER  "$DOCKER_COMPOSE_BUILD_PATH"/manage.py "$DOCKER_COMPOSE_BUILD_PATH"/"$DOCKER_COMPOSE_PROJECT_NAME"

echo -e  "$BLUE""Replacing the DATABASES in the $DOCKER_COMPOSE_BUILD_PATH/$DOCKER_COMPOSE_PROJECT_NAME/settings.py file$NC"

DATABASE_TO_CHANGE=$(cat << EOF
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': BASE_DIR / 'db.sqlite3',
      }
  }
EOF
)
DATABASE_TO_REPLACE=$(cat << EOF
  import os
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql',
          'NAME': os.environ.get('POSTGRES_NAME'),
          'USER': os.environ.get('POSTGRES_USER'),
          'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
          'HOST': os.environ.get('POSTGRES_HOST'),
          'PORT': 5432,
      }
  }
EOF
)

echo -e  "FROM$RED\n$DATABASE_TO_CHANGE\n$NC" "TO$GREEN\n$DATABASE_TO_REPLACE$NC"

