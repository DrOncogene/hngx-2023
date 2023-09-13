from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi import FastAPI

from db import DB
from api.models import PersonIn, PersonOut, Person


app = FastAPI()

db = DB()
db.load()


@app.get("/api/{person_id}")
def get_person(person_id: str) -> PersonOut:
    """
    get a person resource
    """
    person = db.get_by_id(person_id) or db.get_by_name(
        person_id) or db.get_by_email(person_id)
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")

    return person


@app.post("/api", status_code=201)
def create_person(data: PersonIn, resp: JSONResponse) -> PersonOut:
    """
    creates a new person resource
    """
    name = data.name
    email = data.email
    person = Person(name=name, email=email)

    db.new(person)
    try:
        db.save()
    except Exception as err:
        print(err)
        raise HTTPException(
            status_code=400, detail="Email or name already exists")

    return db.get_by_name(name)


@app.put("/api/{person_id}")
def update_person(person_id: str, data: dict) -> PersonOut:
    """
    updates a person resource
    """
    person = db.get_by_id(person_id) or db.get_by_name(
        person_id) or db.get_by_email(person_id)
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")

    if data.get("id"):
        del data["id"]

    for key, value in data.items():
        setattr(person, key, value)

    try:
        db.save()
    except Exception as err:
        print(err)
        raise HTTPException(
            status_code=400, detail="Email or name already exists")

    return person


@app.delete("/api/{person_id}")
def delete_person(person_id: str) -> JSONResponse:
    """
    deletes a person resource
    """
    person = db.get_by_id(person_id) or db.get_by_name(
        person_id) or db.get_by_email(person_id)
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")

    db.delete(person)
    db.save()

    return JSONResponse(
        {"detail": "Person deleted successfully"},
        status_code=200
    )
