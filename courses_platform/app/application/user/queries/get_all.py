from app.domain.user import User
from app.persistence.database.user import user_model as um
from app.application.interfaces.idb_session import DbSession
from app.application.interfaces.icommand_query import ICommandQuery

from app.response_objects import Response, ResponseFailure, ResponseSuccess


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
