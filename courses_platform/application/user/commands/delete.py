from courses_platform.request_objects import Request
from courses_platform.response_objects import Response, ResponseFailure, ResponseSuccess

from courses_platform.application.interfaces.icommand_query import ICommandQuery
from courses_platform.application.interfaces.iuser_repository import URepository


class DeleteUserCommand(ICommandQuery):
    def __init__(self, repo: URepository) -> None:
        self.repo = repo

    def execute(self, request: Request) -> Response:
        if not request:
            return ResponseFailure.build_from_invalid_request(request)

        try:
            result = self.repo.delete_user(user_id=request.user_id)
            return ResponseSuccess(result)
        except Exception as exc:
            return ResponseFailure.build_resource_error(exc)
