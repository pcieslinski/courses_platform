import abc
from typing import List, NewType

from courses_platform.domain.course import Course


class ICourseRepository(abc.ABC):

    @abc.abstractmethod
    def create_course(self, name: str) -> Course:
        pass

    @abc.abstractmethod
    def delete_course(self, course_id: str) -> bool:
        pass

    @abc.abstractmethod
    def get_course(self, course_id: str) -> Course:
        pass

    @abc.abstractmethod
    def get_all_courses(self) -> List[Course]:
        pass


CRepository = NewType('CRepository', ICourseRepository)
