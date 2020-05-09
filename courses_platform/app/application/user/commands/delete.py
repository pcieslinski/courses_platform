from typing import cast, Union

from app.request_objects.invalid_request import InvalidRequest
from app.request_objects.user.delete_user_request import DeleteUserRequest
from app.response_objects import Response, ResponseFailure, ResponseSuccess

from app.domain.user import User
from app.application import exceptions as ex
from app.application.interfaces.iunit_of_work import IUnitOfWork
from app.application.interfaces.icommand_query import ICommandQuery


Request = Union[DeleteUserRequest, InvalidRequest]


class DeleteUserCommand(ICommandQuery):
    def __init__(self, unit_of_work: IUnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    def execute(self, request: Request) -> Response:
        if isinstance(request, InvalidRequest):
            return ResponseFailure.build_from_invalid_request(request)

        try:
            with self.unit_of_work as uow:
                user = cast(User, uow.users.get(request.user_id))

                if user:
                    user.clear_enrollments()
                    uow.users.remove(user)
                else:
                    return ResponseFailure.build_resource_error(
                        ex.NoMatchingUser(request.user_id)
                    )

            return ResponseSuccess.build_response_no_content()

        except Exception as exc:
            return ResponseFailure.build_system_error(exc)
