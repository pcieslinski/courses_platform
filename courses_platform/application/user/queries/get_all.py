from courses_platform.domain.user import User
from courses_platform.persistence.database import user as um
from courses_platform.application.interfaces.idb_session import DbSession
from courses_platform.application.interfaces.icommand_query import ICommandQuery

from courses_platform.response_objects import Response, ResponseFailure, ResponseSuccess


class GetAllUsersQuery(ICommandQuery):
    def __init__(self, db_session: DbSession) -> None:
        self.db_session = db_session

    def execute(self) -> Response:
        try:
            with self.db_session() as db:
                result = db.query(um.User).\
                            all()

                return ResponseSuccess.build_response_success(
                    [
                        User.from_record(user_record)
                        for user_record in result
                    ]
                )

        except Exception as exc:
            return ResponseFailure.build_system_error(exc)
