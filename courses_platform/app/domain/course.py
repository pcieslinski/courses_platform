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
