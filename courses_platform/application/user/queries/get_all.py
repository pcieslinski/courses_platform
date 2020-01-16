from typing import List

from courses_platform.domain.user import User
from courses_platform.application.interfaces.icommand_query import ICommandQuery
from courses_platform.application.interfaces.iuser_repository import URepository


class GetAllUsersQuery(ICommandQuery):
    def __init__(self, repo: URepository) -> None:
        self.repo = repo

    def execute(self) -> List[User]:
        users = self.repo.get_all_users()
        return users
