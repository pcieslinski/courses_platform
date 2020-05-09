import pytest
from typing import Dict, Generator, List, Union

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker, clear_mappers, Session

from app.domain.user import User
from app.domain.course import Course
from app.persistence.orm import metadata, start_mappers
from app.persistence.unit_of_work import SqlAlchemyUnitOfWork


@pytest.fixture
def user() -> User:
    return User('test@gmail.com')


@pytest.fixture
def course() -> Course:
    return Course(name='Test Course')


@pytest.fixture
def users() -> List[User]:
    user_1 = User('test@gmail.com')
    user_2 = User('sample@gmail.com')

    return [
        user_1,
        user_2
    ]


@pytest.fixture
def courses() -> List[Course]:
    course_1 = Course('Test Course')
    course_2 = Course('Sample Course')

    return [
        course_1,
        course_2
    ]


@pytest.fixture
def courses_with_enrollments() -> List[Dict[str, Union[Course, int]]]:
    return [
            {
                'course': Course('Test Course'),
                'enrollments': 10
            }
        ]


@pytest.fixture
def in_memory_db() -> Engine:
    engine = create_engine('sqlite:///:memory:')
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session_factory(in_memory_db) -> Generator[sessionmaker, None, None]:
    start_mappers()
    yield sessionmaker(bind=in_memory_db)
    clear_mappers()


@pytest.fixture
def session(session_factory) -> Session:
    return session_factory()


@pytest.fixture
def uow(session_factory) -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(session_factory)
