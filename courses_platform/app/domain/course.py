from uuid import uuid4
from typing import Type, TypeVar


C = TypeVar('C', bound='Course')


class Course:
    def __init__(self, name: str, id: str = None) -> None:
        self.id = id or str(uuid4())
        self.name = name

    @classmethod
    def from_dict(cls: Type[C], adict: dict) -> C:
        return cls(adict['name'])

    @classmethod
    def from_record(cls: Type[C], record) -> C:
        return cls(
            name=record.name,
            id=record.id
        )
