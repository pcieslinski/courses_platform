from courses_platform.application.interfaces.icommand_query import ICommandQuery
from courses_platform.application.interfaces.iuser_repository import URepository


class NoMatchingUser(Exception):
    pass


class DeleteUserCommand(ICommandQuery):
    def __init__(self, repo: URepository) -> None:
        self.repo = repo

    def execute(self, user_id: str) -> bool:
        result = self.repo.delete_user(user_id=user_id)

        if result:
            return result
        else:
            raise NoMatchingUser(f'No match for User with id {user_id}.')
