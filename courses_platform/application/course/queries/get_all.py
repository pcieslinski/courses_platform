from typing import List

from courses_platform.domain.course import Course
from courses_platform.application.interfaces.icommand_query import ICommandQuery


class GetAllCoursesQuery(ICommandQuery):
    def __init__(self, repo) -> None:
        self.repo = repo

    def execute(self) -> List[Course]:
        courses = self.repo.get_all_courses()
        return courses
