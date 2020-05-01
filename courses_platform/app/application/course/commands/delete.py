from typing import Union

from app.request_objects.invalid_request import InvalidRequest
from app.response_objects import Response, ResponseFailure, ResponseSuccess
from app.request_objects.course.delete_course_request import DeleteCourseRequest

from app.domain.course import Course
from app.application.interfaces.idb_session import DbSession
from app.application.course.exceptions import NoMatchingCourse
from app.application.interfaces.icommand_query import ICommandQuery


Request = Union[DeleteCourseRequest, InvalidRequest]


class DeleteCourseCommand(ICommandQuery):
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

                if course:
                    self.clear_enrollments(course)
                    db.delete(course)
                else:
                    return ResponseFailure.build_resource_error(
                        NoMatchingCourse(
                            f'No Course has been found for a given id: {request.course_id}')
                    )

            return ResponseSuccess.build_response_no_content()

        except Exception as exc:
            return ResponseFailure.build_system_error(exc)

    def clear_enrollments(self, course: Course) -> None:
        course.enrollments = []
