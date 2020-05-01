from typing import Union

from app.request_objects.invalid_request import InvalidRequest
from app.request_objects.user.create_user_request import CreateUserRequest
from app.response_objects import Response, ResponseFailure, ResponseSuccess

from app.domain.user import User
from app.application.interfaces.idb_session import DbSession
from app.application.interfaces.icommand_query import ICommandQuery


Request = Union[CreateUserRequest, InvalidRequest]


class CreateUserCommand(ICommandQuery):
    def __init__(self, db_session: DbSession) -> None:
        self.db_session = db_session

    def execute(self, request: Request) -> Response:
        if isinstance(request, InvalidRequest):
            return ResponseFailure.build_from_invalid_request(request)

        try:
            with self.db_session() as db:
                new_user = User(email=request.email)
                db.add(new_user)

            return ResponseSuccess.build_response_resource_created(new_user)

        except Exception as exc:
            return ResponseFailure.build_resource_error(exc)
