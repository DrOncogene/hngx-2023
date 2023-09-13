from uuid import uuid4

from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import String


class PersonOut(BaseModel):
    """Pydantic model for Person responses"""
    id: str
    name: str
    email: str


class PersonIn(BaseModel):
    """Pydantic model for Person requests"""
    name: str
    email: str


class Base(DeclarativeBase):
    pass


class Person(Base):
    """SQLAlchemy model for Person in db"""
    __tablename__ = "person"

    def gen_id() -> str:
        return str(uuid4())

    id: Mapped[str] = mapped_column(primary_key=True, default=gen_id)
    name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
