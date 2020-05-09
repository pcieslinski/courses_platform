from typing import cast, Union

from app.request_objects.invalid_request import InvalidRequest
from app.response_objects import Response, ResponseFailure, ResponseSuccess
from app.request_objects.course.enrollment_request import EnrollmentRequest

from app.domain.user import User
from app.domain.course import Course
from app.application import exceptions as ex
from app.application.interfaces.iunit_of_work import IUnitOfWork
from app.application.interfaces.icommand_query import ICommandQuery

Request = Union[EnrollmentRequest, InvalidRequest]


class EnrollUserCommand(ICommandQuery):
    def __init__(self, unit_of_work: IUnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    def execute(self, request: Request) -> Response:
        if isinstance(request, InvalidRequest):
            return ResponseFailure.build_from_invalid_request(request)

        try:
            with self.unit_of_work as uow:
                course = cast(Course, uow.courses.get(request.course_id))

                if not course:
                    return ResponseFailure.build_resource_error(
                        ex.NoMatchingCourse(request.course_id)
                    )

                user = cast(User, uow.users.get(request.user_id, load_relation='courses'))

                if not user:
                    return ResponseFailure.build_resource_error(
                        ex.NoMatchingUser(request.user_id)
                    )

                if self.user_is_enrolled(course, user):
                    return ResponseFailure.build_resource_error(
                        ex.UserAlreadyEnrolled(request.user_id, request.course_id)
                    )

                course.enrollments.append(user)

                return ResponseSuccess.build_response_resource_created(
                    {
                        'course_id': request.course_id,
                        'user_id': request.user_id
                    }
                )
        except Exception as exc:
            return ResponseFailure.build_system_error(exc)

    @staticmethod
    def user_is_enrolled(course: Course, user: User) -> bool:
        return True if user in course.enrollments else False
