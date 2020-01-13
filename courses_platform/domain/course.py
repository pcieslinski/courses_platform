from uuid import uuid4
from typing import Type, TypeVar


C = TypeVar('C', bound='Course')


class Course:
    def __init__(self, name: str) -> None:
        self.id = str(uuid4())
        self.name = name

    @classmethod
    def from_dict(cls: Type[C], adict: dict) -> C:
        return cls(adict['name'])
