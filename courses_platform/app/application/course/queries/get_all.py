from typing import List, Union

from app.request_objects.invalid_request import InvalidRequest
from app.response_objects import Response, ResponseFailure, ResponseSuccess
from app.request_objects.course.get_all_courses_request import GetAllCoursesRequest

from app.domain.course import Course
from app.application.interfaces.idb_session import DbSession
from app.application.interfaces.icommand_query import ICommandQuery

Request = Union[GetAllCoursesRequest, InvalidRequest]


class GetAllCoursesQuery(ICommandQuery):
    def __init__(self, db_session: DbSession) -> None:
        self.db_session = db_session

    def execute(self, request: Request) -> Response:
        if isinstance(request, InvalidRequest):
            return ResponseFailure.build_from_invalid_request(request)

        try:
            with self.db_session() as db:
                result = db.query(Course)\
                           .all()

                if 'stats' in request.include:
                    return ResponseSuccess.build_response_success(
                        self._format_response(result)
                    )

                return ResponseSuccess.build_response_success(result)

        except Exception as exc:
            return ResponseFailure.build_system_error(exc)

    def _format_response(self, result: List[Course]) -> List[dict]:
        return [
            {
                'course': course,
                'enrollments': course.enrollments.count()  # type: ignore
            }
            for course in result
        ]
