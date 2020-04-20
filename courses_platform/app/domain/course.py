from __future__ import annotations

from uuid import uuid4


class Course:
    def __init__(self, name: str, id: str = None) -> None:
        self.id = id or str(uuid4())
        self.name = name

    @classmethod
    def from_dict(cls, adict: dict) -> Course:
        return cls(adict['name'])

    @classmethod
    def from_record(cls, record) -> Course:
        return cls(
            name=record.name,
            id=record.id
        )
