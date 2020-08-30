from __future__ import annotations
from typing import Any

from sqlalchemy import orm

from app.domain.user import User
from app.domain.course import Course
from app.adapters import Session
from app.application.interfaces.iunit_of_work import IUnitOfWork
from app.adapters.repositories import SqlAlchemyRepository


class SqlAlchemyUnitOfWork(IUnitOfWork):
    """
    Unit of work for SQLAlchemy, which ensures transactionality when performing database
    operations with the help of repositories. All failed operations are automatically rollbacked.

    Args:
        - session_factory (orm.sessionmaker): Session factory from sqlalchemy
    """

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
