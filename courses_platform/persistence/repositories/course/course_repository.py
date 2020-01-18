from typing import List

from courses_platform.domain.course import Course
from courses_platform.persistence.database import Session
from courses_platform.persistence.repositories.course import course_model as cm
from courses_platform.application.interfaces.icourse_repository import ICourseRepository


class CourseRepository(ICourseRepository):
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def create_course(self, name: str) -> Course:
        with self.db_session() as db:
            course = Course(name=name)

            db.add(
                cm.Course(
                    id=course.id,
                    name=course.name
                )
            )

            return course

    def delete_course(self, course_id: str) -> bool:
        with self.db_session() as db:
            result = db.query(cm.Course).\
                        filter(cm.Course.id == course_id).\
                        delete()

            return result

    def get_course(self, course_id: str) -> Course:
        with self.db_session() as db:
            result = db.query(cm.Course).\
                        filter(cm.Course.id == course_id).\
                        first()

            return Course.from_record(result)

    def get_all_courses(self) -> List[Course]:
        with self.db_session() as db:
            result = db.query(cm.Course).\
                        all()

            courses = [
                Course.from_record(course_record)
                for course_record in result
            ]

            return courses
