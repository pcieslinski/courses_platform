from __future__ import annotations

from uuid import uuid4
from typing import List

from app.domain.course import Course


class User:
    """
    Domain object for the user. May be enrolled in a course.

    Args:
        - email (str): Email of the given user
        - id (str, optional): User ID, which is automatically generated when creating a new user
        - enrollments (List[Course], optional): List of enrollments for the user's courses
    """

    def __init__(
            self, email: str, id: str = None, courses: List[Course] = None
    ) -> None:
        self.id = id or str(uuid4())
        self.email = email
        self.courses = courses or []

    @classmethod
    def from_dict(cls, adict: dict) -> User:
        return cls(adict['email'])

    def clear_enrollments(self) -> None:
        self.courses = []

    def __repr__(self):
        return f'User: id<{self.id}>, name<{self.email}>'
