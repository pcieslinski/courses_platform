from courses_platform.request_objects import Request
from courses_platform.response_objects import Response, ResponseFailure, ResponseSuccess

from courses_platform.application.user.exceptions import NoMatchingUser
from courses_platform.application.interfaces.icommand_query import ICommandQuery
from courses_platform.application.interfaces.iuser_repository import URepository


class GetUserQuery(ICommandQuery):
    def __init__(self, repo: URepository) -> None:
        self.repo = repo

    def execute(self, request: Request) -> Response:
        if not request:
            return ResponseFailure.build_from_invalid_request(request)

        try:
            user = self.repo.get_user(user_id=request.user_id)

            if not user:
                return ResponseFailure.build_resource_error(
                    NoMatchingUser(f'No User has been found for a given id: {request.user_id}'))

            return ResponseSuccess.build_response_success(user)

        except Exception as exc:
            return ResponseFailure.build_system_error(exc)
