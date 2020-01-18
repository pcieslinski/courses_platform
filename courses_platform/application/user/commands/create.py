from courses_platform.request_objects import Request
from courses_platform.response_objects import Response, ResponseFailure, ResponseSuccess

from courses_platform.application.interfaces.icommand_query import ICommandQuery
from courses_platform.application.interfaces.iuser_repository import URepository


class CreateUserCommand(ICommandQuery):
    def __init__(self, repo: URepository) -> None:
        self.repo = repo

    def execute(self, request: Request) -> Response:
        if not request:
            return ResponseFailure.build_from_invalid_request(request)

        try:
            new_user = self.repo.create_user(email=request.email)
            return ResponseSuccess.build_response_resource_created(new_user)
        except Exception as exc:
            return ResponseFailure.build_resource_error(exc)
