# SIMPLE PERSON API

A simple RESTAPI that performs CRUD operations on a person object

## TECHNOLOGIES

- LANGUAGE: Python 3.11
- Framework: FASTAPI
- DATA VALIDATION: Pydantic
- DATABASE: Sqlite3
- ORM: sqlalchemy v2
- TESTING: Pytest
- APPLICATION SERVER: Uvicorn

## DATA SHAPE

Person object:

```
{
    id: string, unique
    name: string, unique
    email: string, unique
}
```

## UML DIAGRAM

Visit [this board](https://whimsical.com/backend-stage-two-YKnMJ3abo4SDbZBymwj5PB) to view the UML diagrams

## ENDPOINTS

#### READ: **GET /api/{id or name or email}**

- Status codes: 200, 404
- 200: successful read
- 404: person does not exist
- Return: person object on success

#### CREATE: **POST /api**

- Creates a new person object
- Request body: json object with name and email fields
- Status codes: 201, 422, 400
- 201: successful creation
- 422: invalid or incomplete data/json
- 400: person already exists
- Return: created person object on success

#### UPDATE: **PUT /api/{id or name or email}**

- Updates a person object
- Status code: 200, 404, 422, 400
- 200: successful update
- 404: person does not exist
- 422: invalid or incomplete data/json
- 400: person already exists
- Return: a person object on success

#### DELETE: **DELETE /api/{id or name or email}**

- Deletes a person object
- Status code: 200, 404
- 200: successful deletion
- 404: person does not exist

## SAMPLE USAGE

```
Request: POST /api HTTP/1.1 application/json
Body: {
        "name": "John Doe",
        "email": "doe@mail.com"
      }

Response: Status 201
Content: {
            "id": "5fhgdf7dryeyr7ey77hdjfbjdfjdf", # will vary
            "name": "John Doe",
            "email": "doe@mail.com"
        }
```

```
Request: GET /api/5fhgdf7dryeyr7ey77hdjfbjdfjdf HTTP/1.1

Response: Status 200
Content: {
            "id": "5fhgdf7dryeyr7ey77hdjfbjdfjdf", # will vary
            "name": "John Doe",
            "email": "doe@mail.com"
        }
```

```
Request: PUT /api/5fhgdf7dryeyr7ey77hdjfbjdfjdf HTTP/1.1 application/json
Body: {
        "name": "Jane Doe",
    }

Response: Status 200
Content: {
            "id": "5fhgdf7dryeyr7ey77hdjfbjdfjdf", # will vary
            "name": "Jane Doe",
            "email": "doe@mail.com"
        }
```

```
Request: DELETE /api/5fhgdf7dryeyr7ey77hdjfbjdfjdf HTTP/1.1

Response: Status 200
Content: {
        "detail": "Person deleted successfully"
    }
```

## SETUP

- Clone the repository
- cd into the backend/stage_two directory (root of the project)
- Run `pipenv install` to install dependencies
- Run `pipenv shell` to activate the virtual environment
- Run `uvicorn api.main:app` or `python3 wsgi.py` to start the application server
- The application server will be running on http://localhost:8000

## TESTING

- From the backend/stage_two directory (root of the project)
- Set `MODE` environment variable to `test`
- Run `pytest test.py` or `python3 test.py` to run the tests
- Alternatively, run `MODE=test pytest test.py` or `MODE=test python3 test.py` to run the tests in one step without setting the environment variable separately

## AUTO DOCUMENTATION

Check [here](http://person-api.droncogene.com/redoc)

ENJOY!
