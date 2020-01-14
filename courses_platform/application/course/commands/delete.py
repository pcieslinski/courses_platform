from typing import Union

from courses_platform.domain.course import Course
from courses_platform.application.interfaces.icommand_query import ICommandQuery


class NoMatchingCourse(Exception):
    pass


class DeleteCourseCommand(ICommandQuery):
    def __init__(self, repo) -> None:
        self.repo = repo

    def execute(self, course_id: str) -> Union[Course, Exception]:
        try:
            result = self.repo.delete_course(course_id=course_id)
            return result
        except NoMatchingCourse as exc:
            return exc
