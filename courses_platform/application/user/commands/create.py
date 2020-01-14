from typing import Union

from courses_platform.domain.user import User
from courses_platform.application.interfaces.icommand_query import ICommandQuery


class UserAlreadyExists(Exception):
    pass


class CreateUserCommand(ICommandQuery):
    def __init__(self, repo) -> None:
        self.repo = repo

    def execute(self, email: str) -> Union[User, Exception]:
        try:
            new_user = self.repo.create_user(email=email)
            return new_user
        except UserAlreadyExists as exc:
            return exc
