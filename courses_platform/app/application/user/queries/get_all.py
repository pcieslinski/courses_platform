from typing import Union

from app.domain.user import User
from app.application.interfaces.idb_session import DbSession
from app.application.interfaces.icommand_query import ICommandQuery

from app.request_objects.valid_request import ValidRequest
from app.request_objects.invalid_request import InvalidRequest
from app.response_objects import Response, ResponseFailure, ResponseSuccess


Request = Union[InvalidRequest, ValidRequest]


class GetAllUsersQuery(ICommandQuery):
    def __init__(self, db_session: DbSession) -> None:
        self.db_session = db_session

    def execute(self, request: Request = None) -> Response:
        try:
            with self.db_session() as db:
                result = db.query(User)\
                           .all()

                return ResponseSuccess.build_response_success(result)

        except Exception as exc:
            return ResponseFailure.build_system_error(exc)
