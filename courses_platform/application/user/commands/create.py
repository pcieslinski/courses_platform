from typing import Union

from courses_platform.domain.user import User


class UserAlreadyExists(Exception):
    pass


class CreateUserCommand:
    def __init__(self, repo) -> None:
        self.repo = repo

    def execute(self, email: str) -> Union[User, Exception]:
        try:
            new_user = self.repo.create_user(email=email)
            return new_user
        except UserAlreadyExists as exc:
            return exc
