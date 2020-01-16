from typing import Union

from courses_platform.domain.course import Course
from courses_platform.application.interfaces.icommand_query import ICommandQuery
from courses_platform.application.interfaces.icourse_repository import CRepository


class CourseAlreadyExists(Exception):
    pass


class CreateCourseCommand(ICommandQuery):
    def __init__(self, repo: CRepository) -> None:
        self.repo = repo

    def execute(self, name: str) -> Union[Course, Exception]:
        try:
            new_course = self.repo.create_course(name=name)
            return new_course
        except CourseAlreadyExists as exc:
            return exc
