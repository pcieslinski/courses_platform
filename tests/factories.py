from typing import List
from dataclasses import dataclass

from app.domain.course import Course


@dataclass
class CourseRecord:
    id: str
    name: str


@dataclass
class UserRecord:
    id: str
    email: str
    courses: List[CourseRecord]


class StubUser:
    def __init__(self, user_id: str, course_id: str):
        self.id = user_id
        self.email = 'test@gmail.com'
        self.courses = [Course(id=course_id, name='Test Course')]


class StubCourse:
    def __init__(self, course_id: str):
        self.id = course_id
        self.name = 'Test Course'
