## User Management API

This is a simple user management API that allows you to create, read, update and delete users as well as their friends list and blocked list.

## Installation

1. Go to the root directory of the backend services

```bash
cd backend
```

2. Run docker-compose to start the services

```bash
docker-compose -f docker-compose-user-management.yml up
```

3. The API will be available at http://localhost:8080
4. The PostgreSQL database will be available at http://localhost:5432

## Usage

The API has the following endpoints:

### Create User

```http://localhost:8006/user/```

with POST request and the following JSON body:

```json
{
    "name": "John Doe",
    "nickname": "johndoe",
    "email": "johndoe@email.com",
    "avatar": "https://www.example.com/avatar.jpg"
}

```

### Get User

```http://localhost:8006/user/{id}```

with GET request

### Get All Users

```http://localhost:8006/user/```

with GET request

### Update User

```http://localhost:8006/user/{id}```

with PATCH request and the following JSON body:

```json
{
    "[field]": "[value]"
}

```

### Delete User

```http://localhost:8006/user/{id}```

with DELETE request

### Add Friend

```http://localhost:8006/user/{id}/friends/{friendId}```

with POST request

### Remove Friend

```http://localhost:8006/user/{id}/friends/{friendId}```

with DELETE request

### Get Friends

```http://localhost:8006/user/{id}/friends```

with GET request

### Block User

```http://localhost:8006/user/{id}/block/{blockId}```

with POST request

### Unblock User

```http://localhost:8006/user/{id}/block/{blockId}```

with DELETE request

### Get Blocked Users

```http://localhost:8006/user/{id}/block```


## Run Tests

To run the tests, go to the root directory of the backend services and run the following command:

```bash
docker-compose -f docker-compose-user-management.yml run user_management_api python3 manage.py test user_management_api
```

## Frontend

The frontend for this API can be started by goiung to the root directory of the frontend services and running the following command:

```bash
npm install -g http-server
http-server
```

The frontend will be available at http://localhost:8080 and will allow you to interact with the API.


