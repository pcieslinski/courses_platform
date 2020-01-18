from courses_platform.application.interfaces.icommand_query import ICommandQuery
from courses_platform.application.interfaces.icourse_repository import CRepository

from courses_platform.response_objects import Response, ResponseFailure, ResponseSuccess


class GetAllCoursesQuery(ICommandQuery):
    def __init__(self, repo: CRepository) -> None:
        self.repo = repo

    def execute(self) -> Response:
        try:
            courses = self.repo.get_all_courses()
            return ResponseSuccess.build_response_success(courses)
        except Exception as exc:
            return ResponseFailure.build_system_error(exc)
