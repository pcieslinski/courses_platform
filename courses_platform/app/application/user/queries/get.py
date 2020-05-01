from typing import Union

from app.request_objects.invalid_request import InvalidRequest
from app.request_objects.user.get_user_request import GetUserRequest
from app.response_objects import Response, ResponseFailure, ResponseSuccess

from app.domain.user import User
from app.application.user.exceptions import NoMatchingUser
from app.application.interfaces.idb_session import DbSession
from app.application.interfaces.icommand_query import ICommandQuery


Request = Union[GetUserRequest, InvalidRequest]


class GetUserQuery(ICommandQuery):
    def __init__(self, db_session: DbSession) -> None:
        self.db_session = db_session

    def execute(self, request: Request) -> Response:
        if isinstance(request, InvalidRequest):
            return ResponseFailure.build_from_invalid_request(request)

        try:
            with self.db_session() as db:
                user = db.query(User)\
                         .filter_by(id=request.user_id)\
                         .first()

                if not user:
                    return ResponseFailure.build_resource_error(
                        NoMatchingUser(
                            f'No User has been found for a given id: {request.user_id}')
                    )

                return ResponseSuccess.build_response_success(user)

        except Exception as exc:
            return ResponseFailure.build_system_error(exc)
