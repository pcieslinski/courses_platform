from uuid import uuid4

from app.domain.user import User
from app.domain.course import Course
from app.persistence.repositories import SqlAlchemyRepository


class TestSqlAlchemyRepository:

    def test_repository_can_save_an_entity(self, session):
        user = User(email='test@gmail.com')

        repo = SqlAlchemyRepository(session=session, model=User)

        repo.add(user)
        session.commit()

        rows = list(session.execute(
            'SELECT id, email FROM "user"'
        ))

        user_record = rows[0]

        assert user_record.id == user.id
        assert user_record.email == 'test@gmail.com'

    def test_repository_returns_an_entity(self, session):
        user_id = str(uuid4())
        session.execute(
            'INSERT INTO user (id, email) VALUES '
            f'("{user_id}", "test@gmail.com")'
        )

        repo = SqlAlchemyRepository(session=session, model=User)

        user = repo.get(identifier=user_id)

        assert user.id == user_id
        assert user.email == 'test@gmail.com'
        assert user.courses == []

    def test_repository_returns_an_entity_with_loaded_relation(self, session):
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

        repo = SqlAlchemyRepository(session=session, model=User)

        user = repo.get(identifier=user_id, load_relation='courses')
        course = user.courses[0]

        assert user.id == user_id
        assert user.email == 'test@gmail.com'
        assert len(user.courses) == 1
        assert course.id == course_id
        assert course.name == 'Test Course'

    def test_repository_returns_list_of_entities(self, session):
        course_1_id = str(uuid4())
        course_2_id = str(uuid4())
        session.execute(
            'INSERT INTO course (id, name) VALUES '
            f'("{course_1_id}", "Test Course"), '
            f'("{course_2_id}", "Sample Course")'
        )

        repo = SqlAlchemyRepository(session=session, model=Course)

        courses = repo.list()

        assert len(courses) == 2
        assert courses[0].id == course_1_id
        assert courses[0].name == 'Test Course'
        assert courses[1].id == course_2_id
        assert courses[1].name == 'Sample Course'

    def test_repository_deletes_entity(self, session_factory):
        course_id = str(uuid4())
        session = session_factory()
        session.execute(
            'INSERT INTO course (id, name) VALUES '
            f'("{course_id}", "Test Course")'
        )
        session.commit()

        new_session = session_factory()
        repo = SqlAlchemyRepository(session=new_session, model=Course)

        course = repo.get(course_id)

        repo.remove(entity=course)
        new_session.commit()

        courses = list(session.execute(
            'SELECT id, name FROM "course"'
        ))

        assert courses == []
