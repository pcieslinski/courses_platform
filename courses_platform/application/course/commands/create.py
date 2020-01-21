from app.request_objects import Request
from app.response_objects import Response, ResponseFailure, ResponseSuccess

from app.domain.course import Course
from app.persistence.database.course import course_model as cm
from courses_platform.application.interfaces.idb_session import DbSession
from courses_platform.application.interfaces.icommand_query import ICommandQuery


class CreateCourseCommand(ICommandQuery):
    def __init__(self, db_session: DbSession) -> None:
        self.db_session = db_session

    def execute(self, request: Request) -> Response:
        if not request:
            return ResponseFailure.build_from_invalid_request(request)

        try:
            with self.db_session() as db:
                new_course = Course(name=request.name)

                db.add(
                    cm.Course(
                        id=new_course.id,
                        name=new_course.name
                    )
                )

            return ResponseSuccess.build_response_resource_created(new_course)

        except Exception as exc:
            return ResponseFailure.build_resource_error(exc)
