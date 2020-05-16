from __future__ import annotations

from uuid import uuid4
from typing import List, TYPE_CHECKING


if TYPE_CHECKING:
    from app.domain.user import User


class Course:
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

    def is_enrolled(self, user: User) -> bool:
        return True if user in self.enrollments else False

    def clear_enrollments(self) -> None:
        self.enrollments = []

    def __repr__(self):
        return f'Course: id<{self.id}>, name<{self.name}>'
