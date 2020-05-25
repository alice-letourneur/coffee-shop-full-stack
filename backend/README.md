# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:drinks-detail`
    - `post:drinks`
    - `patch:drinks`
    - `delete:drinks`
6. Create new roles for:
    - Barista
        - can `get:drinks-detail`
    - Manager
        - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 2 users - assign the Barista role to one and Manager role to the other.
    - Sign into each account and make note of the JWT.
    - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
    - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
    - Run the collection and correct any errors.
    - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

### Implement The Server

There are `@TODO` comments throughout the `./backend/src`. We recommend tackling the files in order and from top to bottom:

1. `./src/auth/auth.py`
2. `./src/api.py`


# API Documentation

## Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/.

## Error Handling

The API will return these error types when requests fail:

- 405: Method not allowed
- 400: Bad request
- 404: Not found
- 422: Unprocessable
- 401: Unauthorized
- 403: Not allowed

## Endpoints library

### `GET /drinks`

No authorization headers required.
Returns a list of all drinks with a short description of their composition.

Request example:
```
curl http://127.0.0.1:5000/drinks
```

Response sample:
```
{
  "drinks": [
    {
      "id": 1,
      "recipe": [
        {
          "color": "blue",
          "parts": 1
        }
      ],
      "title": "Water3"
    }
  ],
  "success": true
}
```

### `GET /drinks-detail`

This endpoint is restricted to authenticated users who have the following permission: `get:drinks-detail`
Returns a list of all drinks with the full details of their composition.

Request example:
```
curl http://127.0.0.1:5000/drinks-detail -H 'Authorization: <your_bearer_token>'
```

Response sample:
```
{
  "drinks": [
    {
      "id": 1,
      "recipe": [
        {
          "color": "blue",
          "name": "Water",
          "parts": 1
        }
      ],
      "title": "Water3"
    }
  ],
  "success": true
}
```

### `POST /drinks`

This endpoint is restricted to authenticated users who have the following permission: `post:drinks`
Creates a new drink using the submitted title and recipe params.
Returns the create drink with the full details of its composition and its id.

Request example:

```
curl -X POST 'localhost:5000/drinks' -H 'Content-Type: application/json' -H 'Authorization: <your_bearer_token>' -H 'Content-Type: application/json' -d '{"title": "Capuccino", "recipe": [{"name": "Milk", "color": "white", "parts": 1}, {"name": "Coffee", "color": "black", "parts": 3}]}'
```

Response sample:
```
{
  "drinks": [
    {
      "id": 1,
      "recipe": [
        {
          "color": "white",
          "name": "Milk",
          "parts": 1
        },
        {
          "color": "black",
          "name": "Coffee",
          "parts": 3
        },
      ],
      "title": "Capuccino"
    }
  ],
  "success": true
}
```

### `PATCH /drinks/<id>`

This endpoint is restricted to authenticated users who have the following permission: `patch:drinks`
Updates the drink with the given ID if it exists using the submitted title and recipe params.
Returns the updated drink with the full details of its composition and its id.

Request example:

```
curl -X PATCH 'localhost:5000/drinks' -H 'Content-Type: application/json' -H 'Authorization: <your_bearer_token>' -H 'Content-Type: application/json' -d '{"title": "Mocha", "recipe": [{"name": "Milk", "color": "white", "parts": 1}, {"name": "Coffee", "color": "black", "parts": 2}, {"name": "Chocolate", "color": "brown", "parts": 1}]}'
```

Response sample:
```
{
  "drinks": [
    {
      "id": 1,
      "recipe": [
        {
          "color": "white",
          "name": "Milk",
          "parts": 1
        },
        {
          "color": "black",
          "name": "Coffee",
          "parts": 2
        },
        {
          "color": "brown",
          "name": "Chocolate",
          "parts": 1
        }
      ],
      "title": "Mocha"
    }
  ],
  "success": true
}
```

### `DELETE /drinks/<id>`

This endpoint is restricted to authenticated users who have the following permission: `delete:drinks`
Deletes the drink with the given ID if it exists. Returns the id of the deleted drink.

Request example:

```
curl -X DELETE http://127.0.0.1:5000/drinks/1 -H 'Authorization: <your_bearer_token>'
```

Response sample:
```
{
  "id": "1",
  "success": true
}
```
