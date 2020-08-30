from __future__ import annotations

from uuid import uuid4
from typing import List, TYPE_CHECKING


if TYPE_CHECKING:
    from app.domain.user import User


class Course:
    """
    Domain object for the course. The basic actions available for this object are enrolling
    up and withdrawing users enrollment from the course.

    Args:
        - name (str): Name of the course
        - id (str, optional): Course ID, which is automatically generated when creating a new course
        - enrollments (List[User], optional): List of users who are enrolled in the course
    """

    def __init__(
            self, name: str, id: str = None, enrollments: List[User] = None
    ) -> None:
        self.id = id or str(uuid4())
        self.name = name
        self.enrollments = enrollments or []

    @classmethod
    def from_dict(cls, adict: dict) -> Course:
        return cls(adict['name'])

    @property
    def enrollments_count(self) -> int:
        return len(list(self.enrollments))

    def enroll(self, user: User) -> None:
        self.enrollments.append(user)

    def withdraw_enrollment(self, user: User) -> None:
        self.enrollments.remove(user)

    def is_enrolled(self, user: User) -> bool:
        return True if user in self.enrollments else False

    def clear_enrollments(self) -> None:
        self.enrollments = []

    def __repr__(self):
        return f'Course: id<{self.id}>, name<{self.name}>'
