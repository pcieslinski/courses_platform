from courses_platform.request_objects import Request
from courses_platform.response_objects import Response, ResponseFailure, ResponseSuccess

from courses_platform.persistence.database import user as um
from courses_platform.application.user.exceptions import NoMatchingUser
from courses_platform.application.interfaces.idb_session import DbSession
from courses_platform.application.interfaces.icommand_query import ICommandQuery


class DeleteUserCommand(ICommandQuery):
    def __init__(self, db_session: DbSession) -> None:
        self.db_session = db_session

    def execute(self, request: Request) -> Response:
        if not request:
            return ResponseFailure.build_from_invalid_request(request)

        try:
            with self.db_session() as db:
                result = db.query(um.User).\
                            filter(um.User.id == request.user_id).\
                            delete()

            if not result:
                return ResponseFailure.build_resource_error(
                    NoMatchingUser(
                        f'No User has been found for a given id: {request.user_id}')
                )

            return ResponseSuccess.build_response_no_content()

        except Exception as exc:
            return ResponseFailure.build_system_error(exc)
