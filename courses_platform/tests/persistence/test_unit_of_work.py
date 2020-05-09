import pytest
from uuid import uuid4

from app.domain.course import Course
from app.persistence.unit_of_work import SqlAlchemyUnitOfWork


class TestSqlAlchemyUnitOfWork:

    def test_unit_of_work_can_retrieve_course_and_enroll_user_on_it(self, session_factory):
        course_id = str(uuid4())
        user_id = str(uuid4())

        session = session_factory()
        session.execute(
            'INSERT INTO course (id, name) VALUES '
            f'("{course_id}", "Test Course")'
        )
        session.execute(
            'INSERT INTO user (id, email) VALUES '
            f'("{user_id}", "test@gmail.com")'
        )
        session.commit()

        uow = SqlAlchemyUnitOfWork(session_factory=session_factory)

        with uow:
            course = uow.courses.get(course_id)
            user = uow.users.get(user_id)

            course.enrollments.append(user)

        enrollments = list(session.execute(
            'SELECT course_id, user_id FROM "enrollment"'
        ))

        assert len(enrollments) == 1
        assert enrollments[0][0] == course_id
        assert enrollments[0][1] == user.id

    def test_unit_of_work_rolls_back_transaction_on_error(self, session_factory):
        uow = SqlAlchemyUnitOfWork(session_factory=session_factory)

        with pytest.raises(Exception):
            with uow:
                course = Course(name='Test Course')

                uow.courses.add(course)
                raise Exception

        new_session = session_factory()
        courses = list(new_session.execute('SELECT * FROM "course"'))

        assert courses == []
