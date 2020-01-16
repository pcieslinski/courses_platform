from courses_platform.application.interfaces.icommand_query import ICommandQuery
from courses_platform.application.interfaces.icourse_repository import CRepository


class NoMatchingCourse(Exception):
    pass


class DeleteCourseCommand(ICommandQuery):
    def __init__(self, repo: CRepository) -> None:
        self.repo = repo

    def execute(self, course_id: str) -> bool:
        result = self.repo.delete_course(course_id=course_id)

        if result:
            return result
        else:
            raise NoMatchingCourse(f'No match for Course with id {course_id}.')
