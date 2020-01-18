from courses_platform.request_objects import Request
from courses_platform.response_objects import Response, ResponseFailure, ResponseSuccess

from courses_platform.application.course.exceptions import NoMatchingCourse
from courses_platform.application.interfaces.icommand_query import ICommandQuery
from courses_platform.application.interfaces.icourse_repository import CRepository


class GetCourseQuery(ICommandQuery):
    def __init__(self, repo: CRepository) -> None:
        self.repo = repo

    def execute(self, request: Request) -> Response:
        if not request:
            return ResponseFailure.build_from_invalid_request(request)

        try:
            course = self.repo.get_course(course_id=request.course_id)

            if not course:
                return ResponseFailure.build_resource_error(
                    NoMatchingCourse(f'No Course has been found for a given id: {request.course_id}'))

            return ResponseSuccess.build_response_success(course)

        except Exception as exc:
            return ResponseFailure.build_system_error(exc)
