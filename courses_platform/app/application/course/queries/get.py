from typing import Union

from app.request_objects.invalid_request import InvalidRequest
from app.request_objects.course.get_course_request import GetCourseRequest
from app.response_objects import Response, ResponseFailure, ResponseSuccess

from app.domain.course import Course
from app.application.interfaces.idb_session import DbSession
from app.application.course.exceptions import NoMatchingCourse
from app.application.interfaces.icommand_query import ICommandQuery


Request = Union[GetCourseRequest, InvalidRequest]


class GetCourseQuery(ICommandQuery):
    def __init__(self, db_session: DbSession) -> None:
        self.db_session = db_session

    def execute(self, request: Request) -> Response:
        if isinstance(request, InvalidRequest):
            return ResponseFailure.build_from_invalid_request(request)

        try:
            with self.db_session() as db:
                course = db.query(Course)\
                           .filter_by(id=request.course_id)\
                           .first()

                if not course:
                    return ResponseFailure.build_resource_error(
                        NoMatchingCourse(
                            f'No Course has been found for a given id: {request.course_id}')
                    )

                return ResponseSuccess.build_response_success(course)

        except Exception as exc:
            return ResponseFailure.build_system_error(exc)
