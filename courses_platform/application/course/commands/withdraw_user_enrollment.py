from courses_platform.request_objects import Request
from courses_platform.response_objects import Response, ResponseFailure, ResponseSuccess

from app.persistence.database.user import user_model as um
from app.persistence.database.course import course_model as cm
from courses_platform.application.course import exceptions as ex
from courses_platform.application.user.exceptions import NoMatchingUser
from courses_platform.application.interfaces.idb_session import DbSession
from courses_platform.application.interfaces.icommand_query import ICommandQuery


class WithdrawUserEnrollmentCommand(ICommandQuery):
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

                if not self.user_is_enrolled(course, user):
                    return ResponseFailure.build_resource_error(
                        ex.UserNotEnrolled(
                            f'User: {request.user_id} is not enrolled in Course: {request.course_id}'))

                course.enrollments.remove(user)

                return ResponseSuccess.build_response_no_content()
        except Exception as exc:
            return ResponseFailure.build_system_error(exc)
