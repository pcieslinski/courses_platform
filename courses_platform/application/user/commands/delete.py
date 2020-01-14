from typing import Union

from courses_platform.domain.user import User


class NoMatchingUser(Exception):
    pass


class DeleteUserCommand:
    def __init__(self, repo) -> None:
        self.repo = repo

    def execute(self, user_id: str) -> Union[User, Exception]:
        try:
            result = self.repo.delete_user(user_id=user_id)
            return result

        except NoMatchingUser as exc:
            return exc
