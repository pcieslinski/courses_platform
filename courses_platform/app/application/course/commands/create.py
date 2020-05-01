from typing import Union

from app.request_objects.invalid_request import InvalidRequest
from app.response_objects import Response, ResponseFailure, ResponseSuccess
from app.request_objects.course.create_course_request import CreateCourseRequest

from app.domain.course import Course
from app.application.interfaces.idb_session import DbSession
from app.application.interfaces.icommand_query import ICommandQuery


Request = Union[CreateCourseRequest, InvalidRequest]


class CreateCourseCommand(ICommandQuery):
    def __init__(self, db_session: DbSession) -> None:
        self.db_session = db_session

    def execute(self, request: Request) -> Response:
        if isinstance(request, InvalidRequest):
            return ResponseFailure.build_from_invalid_request(request)

        try:
            with self.db_session() as db:
                new_course = Course(name=request.name)
                db.add(new_course)

            return ResponseSuccess.build_response_resource_created(new_course)

        except Exception as exc:
            return ResponseFailure.build_resource_error(exc)
