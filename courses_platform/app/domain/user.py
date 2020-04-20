from __future__ import annotations

from uuid import uuid4
from typing import List

from app.domain.course import Course


class User:
    def __init__(self, email: str, id: str = None, courses: List[Course] = None) -> None:
        self.id = id or str(uuid4())
        self.email = email
        self.courses = courses or []

    @classmethod
    def from_dict(cls, adict: dict) -> User:
        return cls(adict['email'])

    @classmethod
    def from_record(cls, record) -> User:
        return cls(
            email=record.email,
            id=record.id,
            courses=[
                Course.from_record(course)
                for course in record.courses
            ]
        )
