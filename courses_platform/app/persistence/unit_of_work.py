from __future__ import annotations
from typing import Any

from sqlalchemy import orm

from app.domain.user import User
from app.domain.course import Course
from app.persistence import Session
from app.application.interfaces.iunit_of_work import IUnitOfWork
from app.persistence.repositories import SqlAlchemyRepository


class SqlAlchemyUnitOfWork(IUnitOfWork):
    def __init__(
            self, session_factory: orm.sessionmaker = Session) -> None:
        self.session_factory = session_factory

    def __enter__(self) -> SqlAlchemyUnitOfWork:
        self.session = self.session_factory()  # type: orm.Session
        self.users = SqlAlchemyRepository(self.session, model=User)
        self.courses = SqlAlchemyRepository(self.session, model=Course)

        return self

    def __exit__(self, *args: Any) -> None:
        if any(args):
            self.session.rollback()
        else:
            self.session.commit()
