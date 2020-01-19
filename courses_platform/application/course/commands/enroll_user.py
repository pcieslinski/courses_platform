from courses_platform.request_objects import Request
from courses_platform.response_objects import Response, ResponseFailure, ResponseSuccess

from courses_platform.persistence.database import user as um
from courses_platform.persistence.database import course as cm
from courses_platform.application.course import exceptions as ex
from courses_platform.application.user.exceptions import NoMatchingUser
from courses_platform.application.interfaces.idb_session import DbSession
from courses_platform.application.interfaces.icommand_query import ICommandQuery


class EnrollUserCommand(ICommandQuery):
    def __init__(self, db_session: DbSession) -> None:
        self.db_session = db_session

    @staticmethod
    def user_is_enrolled(course: cm.Course, user: um.User) -> bool:
        return True if user in course.enrollments else False

    def execute(self, request: Request) -> Response:
        if not request:
            return ResponseFailure.build_from_invalid_request(request)

        try:
            with self.db_session() as db:
                course = db.query(cm.Course). \
                            filter(cm.Course.id == request.course_id). \
                            first()

                if not course:
                    return ResponseFailure.build_resource_error(
                        ex.NoMatchingCourse(
                            f'No Course has been found for a given id: {request.course_id}'))

                user = db.query(um.User). \
                          filter(um.User.id == request.user_id). \
                          first()

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
