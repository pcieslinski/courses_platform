from uuid import uuid4

from app.domain.user import User
from app.domain.course import Course


class TestUsersMapper:

    def test_users_mapper_can_load_users(self, session):
        user_1_uuid = str(uuid4())
        user_2_uuid = str(uuid4())

        session.execute(
            'INSERT INTO user (id, email) VALUES '
            f'("{user_1_uuid}", "test@gmail.com"), '
            f'("{user_2_uuid}", "dev@gmail.com")'
        )

        users = session.query(User).all()

        assert users[0].id == user_1_uuid
        assert users[0].email == 'test@gmail.com'
        assert users[1].id == user_2_uuid
        assert users[1].email == 'dev@gmail.com'

    def test_users_mapper_can_save_user(self, session):
        user_id = str(uuid4())
        user = User(id=user_id, email='test@gmail.com')

        session.add(user)
        session.commit()

        record = session.query(User).first()

        assert record.id == user_id
        assert record.email == 'test@gmail.com'


class TestCoursesMapper:

    def test_course_mapper_can_load_courses(self, session):
        course_1_uuid = str(uuid4())
        course_2_uuid = str(uuid4())

        session.execute(
            'INSERT INTO course (id, name) VALUES '
            f'("{course_1_uuid}", "Test Course"), '
            f'("{course_2_uuid}", "Sample Course")'
        )

        courses = session.query(Course).all()

        assert courses[0].id == course_1_uuid
        assert courses[0].name == 'Test Course'
        assert courses[1].id == course_2_uuid
        assert courses[1].name == 'Sample Course'

    def test_courses_mapper_can_save_course(self, session):
        course_id = str(uuid4())
        course = Course(id=course_id, name='Test Course')

        session.add(course)
        session.commit()

        record = session.query(Course).first()

        assert record.id == course_id
        assert record.name == 'Test Course'

    def test_courses_mapper_can_create_enrollments(self, session):
        course = Course('Test Course')
        user = User('test@gmail.com')

        course.enrollments.append(user)

        session.add(course)
        session.commit()

        enrollments = list(session.execute(
            'SELECT course_id, user_id FROM "enrollment"'
        ))

        assert enrollments == [(course.id, user.id)]

    def test_courses_mapper_can_retrieve_enrollments(self, session):
        user_id = str(uuid4())
        session.execute(
            'INSERT INTO user (id, email) VALUES '
            f'("{user_id}", "test@gmail.com")'
        )

        course_id = str(uuid4())
        session.execute(
            'INSERT INTO course (id, name) VALUES '
            f'("{course_id}", "Test Course")'
        )

        session.execute(
            'INSERT INTO enrollment (course_id, user_id) VALUES (:course_id, :user_id)',
            dict(course_id=course_id, user_id=user_id)
        )

        course = session.query(Course).first()
        enrollment = course.enrollments[0]

        assert course.enrollments.count() == 1
        assert enrollment.id == user_id
        assert enrollment.email == 'test@gmail.com'
