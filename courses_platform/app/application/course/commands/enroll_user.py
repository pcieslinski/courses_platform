from typing import cast

from app.domain.user import User
from app.domain.course import Course
from app.application import exceptions as ex
from app.application.interfaces.iunit_of_work import IUnitOfWork
from app.response_objects import Response, ResponseFailure, ResponseSuccess


class EnrollUserCommand:
    def __init__(self, unit_of_work: IUnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    def execute(self, course_id: str, user_id: str) -> Response:
        try:
            with self.unit_of_work as uow:
                course = cast(Course, uow.courses.get(course_id))

                if not course:
                    return ResponseFailure.build_resource_error(
                        ex.NoMatchingCourse(course_id)
                    )

                user = cast(User, uow.users.get(user_id, load_relation='courses'))

                if not user:
                    return ResponseFailure.build_resource_error(
                        ex.NoMatchingUser(user_id)
                    )

                if course.is_enrolled(user):
                    return ResponseFailure.build_resource_error(
                        ex.UserAlreadyEnrolled(user_id, course_id)
                    )

                course.enrollments.append(user)

                return ResponseSuccess.build_response_resource_created(
                    {
                        'course_id': course_id,
                        'user_id': user_id
                    }
                )
        except Exception as exc:
            return ResponseFailure.build_system_error(exc)
