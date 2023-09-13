from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from api.models import Base, Person


class DB:
    """db engine"""
    __engine = None
    __session = None
    __session_maker = None
    MODE = getenv('MODE')

    def __init__(self) -> None:
        if self.MODE == "test":
            self.db_name = "test_db.sqlite3"
        else:
            self.db_name = "db.sqlite3"

        self.__engine = create_engine(
            f"sqlite:///./{self.db_name}", pool_pre_ping=True)

        if self.MODE == "test":
            Base.metadata.drop_all(self.__engine)

    def load(self) -> None:
        """load db"""
        Base.metadata.create_all(self.__engine)
        factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False, autoflush=False)
        self.__session_maker = scoped_session(factory)
        self.__session = self.__session_maker()

    def new(self, obj: Person):
        """add a new person to the db"""
        self.__session.add(obj)

    def get_by_id(self, id: str) -> Person:
        """get a person from the db by id"""
        return self.__session.query(Person).filter(Person.id == id).first()

    def get_by_name(self, name: str) -> Person:
        """get a person from the db by name"""
        return self.__session.query(Person).filter(Person.name == name).first()

    def get_by_email(self, email: str) -> Person:
        """get a person from the db by email"""
        return self.__session.query(Person).filter(
            Person.email == email).first()

    def save(self):
        """save db"""
        try:
            self.__session.commit()
        except Exception as err:
            self.__session.rollback()
            raise err

    def delete(self, obj=None):
        """ deletes obj from the current session"""
        if obj is not None:
            self.__session.delete(obj)

    def close(self):
        """ remove the current session and create a new one"""
        self.__session.close()
        self.__session = self.__sessionmaker()
