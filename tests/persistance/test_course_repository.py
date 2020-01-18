import pytest
from uuid import uuid4
from typing import Tuple
from mock import Mock, patch
from dataclasses import dataclass

from courses_platform.domain.course import Course
from courses_platform.persistence.repositories.course.course_repository import CourseRepository


@pytest.fixture
def db(course_record: dataclass) -> Mock:
    db = Mock()

    db.query.return_value.filter.return_value.delete.return_value = 1
    db.query.return_value.filter.return_value.first.return_value = course_record('1', 'Test Course')
    db.query.return_value.all.return_value = [
        course_record('1', 'Test Course'),
        course_record('2', 'Sample Course')
    ]

    return db


@pytest.fixture(scope='function')
@patch('courses_platform.persistence.database.session', autospec=True)
def mock_session_with_db(session: Mock, db: Mock) -> Tuple[Mock, Mock]:
    session.return_value.__enter__.return_value = db
    return session, db


@pytest.fixture(scope='function')
def course_repo_with_mocks(mock_session_with_db: Tuple[Mock, Mock]) -> Tuple[Mock, Mock, Mock]:
    mock_session, db = mock_session_with_db
    repo = CourseRepository(db_session=mock_session)
    return repo, mock_session, db


class TestCourseRepository:

    def test_course_repository_initialize_correctly(self):
        session = Mock()
        repo = CourseRepository(db_session=session)

        assert isinstance(repo, CourseRepository)
        assert hasattr(repo, 'db_session')
        assert repo.db_session is session

    @patch('uuid.UUID')
    def test_course_repository_creates_course(self, mock_uuid, course_repo_with_mocks, course):
        mock_uuid.return_value = course.id
        repo, mock_session, db = course_repo_with_mocks

        result = repo.create_course('Test Course')

        mock_session.assert_called_once()
        db.add.assert_called_once()
        assert result.id == course.id
        assert result.name == course.name

    def test_course_repository_deletes_course(self, course_repo_with_mocks):
        repo, mock_session, db = course_repo_with_mocks

        course_id = str(uuid4())
        result = repo.delete_course(course_id)

        mock_session.assert_called_once()
        db.query.assert_called_once()
        db.query().filter.assert_called_once()
        db.query().filter().delete.assert_called_once()
        assert result == 1

    def test_course_repository_returns_course(self, course_repo_with_mocks):
        repo, mock_session, db = course_repo_with_mocks

        course_id = str(uuid4())
        result = repo.get_course(course_id)

        mock_session.assert_called_once()
        db.query.assert_called_once()
        db.query().filter.assert_called_once()
        db.query().filter().first.assert_called_once()

        assert isinstance(result, Course)
        assert result.id == '1'
        assert result.name == 'Test Course'

    def test_course_repository_returns_list_of_courses(self, course_repo_with_mocks):
        repo, mock_session, db = course_repo_with_mocks

        result = repo.get_all_courses()

        mock_session.assert_called_once()
        db.query.assert_called_once()
        db.query().all.assert_called_once_with()

        assert len(result) == 2
        assert isinstance(result[0], Course)
        assert isinstance(result[1], Course)
