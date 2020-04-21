from typing import Union
from sqlalchemy.orm import selectinload

from app.request_objects.invalid_request import InvalidRequest
from app.response_objects import Response, ResponseFailure, ResponseSuccess
from app.request_objects.course.enrollment_request import EnrollmentRequest

from app.persistence.database.user import user_model as um
from app.persistence.database.course import course_model as cm
from app.application.course import exceptions as ex
from app.application.user.exceptions import NoMatchingUser
from app.application.interfaces.idb_session import DbSession
from app.application.interfaces.icommand_query import ICommandQuery

Request = Union[EnrollmentRequest, InvalidRequest]


class EnrollUserCommand(ICommandQuery):
    def __init__(self, db_session: DbSession) -> None:
        self.db_session = db_session

    @staticmethod
    def user_is_enrolled(course: cm.Course, user: um.User) -> bool:
        return True if user in course.enrollments else False

    def execute(self, request: Request) -> Response:
        if isinstance(request, InvalidRequest):
            return ResponseFailure.build_from_invalid_request(request)

        try:
            with self.db_session() as db:
                course = db.query(cm.Course)\
                           .filter(cm.Course.id == request.course_id)\
                           .first()

                if not course:
                    return ResponseFailure.build_resource_error(
                        ex.NoMatchingCourse(
                            f'No Course has been found for a given id: {request.course_id}'))

                user = db.query(um.User)\
                         .options(selectinload('courses'))\
                         .filter(um.User.id == request.user_id)\
                         .first()

                if not user:
                    return ResponseFailure.build_resource_error(
                        NoMatchingUser(
                            f'No User has been found for a given id: {request.user_id}'))

                if self.user_is_enrolled(course, user):
                    return ResponseFailure.build_resource_error(
                        ex.UserAlreadyEnrolled(
                            f'User: {request.user_id} is already enrolled in Course: {request.course_id}'))

                course.enrollments.append(user)

                return ResponseSuccess.build_response_resource_created(
                    {
                        'course_id': request.course_id,
                        'user_id': request.user_id
                    }
                )
        except Exception as exc:
            return ResponseFailure.build_system_error(exc)
