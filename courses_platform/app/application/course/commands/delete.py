from typing import cast, Union

from app.request_objects.invalid_request import InvalidRequest
from app.response_objects import Response, ResponseFailure, ResponseSuccess
from app.request_objects.course.delete_course_request import DeleteCourseRequest

from app.domain.course import Course
from app.application.course.exceptions import NoMatchingCourse
from app.application.interfaces.iunit_of_work import IUnitOfWork
from app.application.interfaces.icommand_query import ICommandQuery


Request = Union[DeleteCourseRequest, InvalidRequest]


class DeleteCourseCommand(ICommandQuery):
    def __init__(self, unit_of_work: IUnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    def execute(self, request: Request) -> Response:
        if isinstance(request, InvalidRequest):
            return ResponseFailure.build_from_invalid_request(request)

        try:
            with self.unit_of_work as uow:
                course = cast(Course, uow.courses.get(request.course_id))

                if course:
                    self.clear_enrollments(course)
                    uow.courses.remove(course)
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
