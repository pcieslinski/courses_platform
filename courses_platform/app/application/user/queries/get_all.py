from typing import List
from sqlalchemy.orm import selectinload

from app.domain.user import User
from app.persistence.database.user import user_model as um
from app.application.interfaces.idb_session import DbSession
from app.application.interfaces.icommand_query import ICommandQuery

from app.response_objects import Response, ResponseFailure, ResponseSuccess


class GetAllUsersQuery(ICommandQuery):
    def __init__(self, db_session: DbSession) -> None:
        self.db_session = db_session

    def _create_users_objects(self, result: List[um.User], include_courses: bool = False) -> List[User]:
        users_objects = [
            User.from_record(user_record)
            for user_record in result
        ]

        if not include_courses:
            for user_obj in users_objects:
                del user_obj.courses

        return users_objects

    def execute(self) -> Response:
        try:
            with self.db_session() as db:
                result = db.query(um.User).\
                            options(selectinload('courses')).\
                            all()

                return ResponseSuccess.build_response_success(
                    self._create_users_objects(result)
                )

        except Exception as exc:
            return ResponseFailure.build_system_error(exc)
