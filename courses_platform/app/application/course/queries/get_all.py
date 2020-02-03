from sqlalchemy import func
from typing import List, Tuple

from app.request_objects import Request
from app.response_objects import Response, ResponseFailure, ResponseSuccess

from app.domain.course import Course
from app.persistence.database.course import course_model as cm
from app.application.interfaces.idb_session import DbSession
from app.application.interfaces.icommand_query import ICommandQuery


class GetAllCoursesQuery(ICommandQuery):
    def __init__(self, db_session: DbSession) -> None:
        self.db_session = db_session

    def _create_courses_objects(self, result: List[cm.Course]) -> List[Course]:
        return [
            Course.from_record(course_record)
            for course_record in result
        ]

    def _create_courses_objects_with_stats(self, result: List[Tuple[cm.Course, int]]) -> List[dict]:
        return [
            {
                'course': Course.from_record(course),
                'enrollments': n_enrollments
            }
            for course, n_enrollments in result
        ]

    def execute(self, request: Request) -> Response:
        if not request:
            return ResponseFailure.build_from_invalid_request(request)

        try:
            with self.db_session() as db:

                if 'stats' in request.include:
                    result = db.query(cm.Course, func.count(cm.Course.id)).\
                                outerjoin(cm.Course.enrollments).\
                                group_by(cm.Course.id).\
                                all()

                    return ResponseSuccess.build_response_success(
                        self._create_courses_objects_with_stats(result)
                    )

                result = db.query(cm.Course).\
                            all()

                return ResponseSuccess.build_response_success(
                    self._create_courses_objects(result)
                )

        except Exception as exc:
            return ResponseFailure.build_system_error(exc)
