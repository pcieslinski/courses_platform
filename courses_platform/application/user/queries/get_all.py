from courses_platform.application.interfaces.icommand_query import ICommandQuery
from courses_platform.application.interfaces.iuser_repository import URepository

from courses_platform.response_objects import Response, ResponseFailure, ResponseSuccess


class GetAllUsersQuery(ICommandQuery):
    def __init__(self, repo: URepository) -> None:
        self.repo = repo

    def execute(self) -> Response:
        try:
            users = self.repo.get_all_users()
            return ResponseSuccess(users)
        except Exception as exc:
            return ResponseFailure.build_system_error(exc)
