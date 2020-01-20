from courses_platform.request_objects import Request
from courses_platform.response_objects import Response, ResponseFailure, ResponseSuccess

from app.domain.user import User
from app.persistence.database.user import user_model as um
from courses_platform.application.interfaces.idb_session import DbSession
from courses_platform.application.interfaces.icommand_query import ICommandQuery


class CreateUserCommand(ICommandQuery):
    def __init__(self, db_session: DbSession) -> None:
        self.db_session = db_session

    def execute(self, request: Request) -> Response:
        if not request:
            return ResponseFailure.build_from_invalid_request(request)

        try:
            with self.db_session() as db:
                new_user = User(email=request.email)

                db.add(
                    um.User(
                        id=new_user.id,
                        email=new_user.email
                    )
                )

            return ResponseSuccess.build_response_resource_created(new_user)

        except Exception as exc:
            return ResponseFailure.build_resource_error(exc)
