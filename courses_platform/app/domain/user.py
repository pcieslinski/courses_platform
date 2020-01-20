from uuid import uuid4
from typing import List, Type, TypeVar

from app.domain.course import Course

U = TypeVar('U', bound='User')


class User:
    def __init__(self, email: str, id: str = None, courses: List[Course] = None) -> None:
        self.id = id or str(uuid4())
        self.email = email
        self.courses = courses or []

    @classmethod
    def from_dict(cls: Type[U], adict: dict) -> U:
        return cls(adict['email'])

    @classmethod
    def from_record(cls: Type[U], record) -> U:
        return cls(
            email=record.email,
            id=record.id,
            courses=record.courses
        )
