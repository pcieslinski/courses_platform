from uuid import uuid4


class User:
    def __init__(self, email: str) -> None:
        self.id = str(uuid4())
        self.email = email

    @classmethod
    def from_dict(cls, adict: dict):
        return cls(adict['email'])
