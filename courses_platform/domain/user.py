from uuid import uuid4
from typing import Type, TypeVar


U = TypeVar('U', bound='User')


class User:
    def __init__(self, email: str, id: str = None) -> None:
        self.id = id or str(uuid4())
        self.email = email

    @classmethod
    def from_dict(cls: Type[U], adict: dict) -> U:
        return cls(adict['email'])

    @classmethod
    def from_record(cls: Type[U], record) -> U:
        return cls(
            email=record.email,
            id=record.id
        )
