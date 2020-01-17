from courses_platform.request_objects import Request
from courses_platform.response_objects import Response, ResponseFailure, ResponseSuccess

from courses_platform.application.interfaces.icommand_query import ICommandQuery
from courses_platform.application.interfaces.icourse_repository import CRepository


class DeleteCourseCommand(ICommandQuery):
    def __init__(self, repo: CRepository) -> None:
        self.repo = repo

    def execute(self, request: Request) -> Response:
        if not request:
            return ResponseFailure.build_from_invalid_request(request)

        try:
            self.repo.delete_course(course_id=request.course_id)
            return ResponseSuccess('')
        except Exception as exc:
            return ResponseFailure.build_resource_error(exc)
