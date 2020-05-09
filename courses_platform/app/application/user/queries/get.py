from typing import Union

from app.request_objects.invalid_request import InvalidRequest
from app.request_objects.user.get_user_request import GetUserRequest
from app.response_objects import Response, ResponseFailure, ResponseSuccess

from app.application.user.exceptions import NoMatchingUser
from app.application.interfaces.iunit_of_work import IUnitOfWork
from app.application.interfaces.icommand_query import ICommandQuery


Request = Union[GetUserRequest, InvalidRequest]


class GetUserQuery(ICommandQuery):
    def __init__(self, unit_of_work: IUnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    def execute(self, request: Request) -> Response:
        if isinstance(request, InvalidRequest):
            return ResponseFailure.build_from_invalid_request(request)

        try:
            with self.unit_of_work as uow:
                user = uow.users.get(request.user_id)

                if not user:
                    return ResponseFailure.build_resource_error(
                        NoMatchingUser(
                            f'No User has been found for a given id: {request.user_id}')
                    )

                return ResponseSuccess.build_response_success(user)

        except Exception as exc:
            return ResponseFailure.build_system_error(exc)
