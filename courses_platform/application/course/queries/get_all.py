from courses_platform.domain.course import Course
from courses_platform.persistence.database import course as cm
from courses_platform.application.interfaces.idb_session import DbSession
from courses_platform.application.interfaces.icommand_query import ICommandQuery

from courses_platform.response_objects import Response, ResponseFailure, ResponseSuccess


class GetAllCoursesQuery(ICommandQuery):
    def __init__(self, db_session: DbSession) -> None:
        self.db_session = db_session

    def execute(self) -> Response:
        try:
            with self.db_session() as db:
                result = db.query(cm.Course).\
                            all()

                return ResponseSuccess.build_response_success(
                    [
                        Course.from_record(course_record)
                        for course_record in result
                    ]
                )

        except Exception as exc:
            return ResponseFailure.build_system_error(exc)
