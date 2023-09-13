from fastapi import FastAPI
from db import DB


def create_app() -> FastAPI:
    """app factory"""
    from api.routes import router

    app = FastAPI()
    app.include_router(router)

    return app


db = DB()
db.load()
