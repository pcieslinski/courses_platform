import pytest
from uuid import uuid4
from mock import Mock, patch

from courses_platform.domain.user import User
from courses_platform.persistence.repositories.user.user_repository import UserRepository


@pytest.fixture
def db(user_record):
    db = Mock()

    db.query.return_value.filter.return_value.delete.return_value = 1
    db.query.return_value.all.return_value = [
        user_record('1', 'test@gmail.com'),
        user_record('2', 'sample@gmail.com')
    ]

    return db


@pytest.fixture(scope='function')
@patch('courses_platform.persistence.database.session', autospec=True)
def mock_session_with_db(session, db):
    session.return_value.__enter__.return_value = db
    return session, db


@pytest.fixture(scope='function')
def user_repo_with_mocks(mock_session_with_db):
    mock_session, db = mock_session_with_db
    repo = UserRepository(db_session=mock_session)
    return repo, mock_session, db


class TestUserRepository:

    def test_user_repository_initialize_correctly(self):
        session = Mock()
        repo = UserRepository(db_session=session)

        assert isinstance(repo, UserRepository)
        assert hasattr(repo, 'db_session')
        assert repo.db_session is session

    @patch('uuid.UUID')
    def test_user_repository_creates_user(self, mock_uuid, user_repo_with_mocks, user):
        mock_uuid.return_value = user.id
        repo, mock_session, db = user_repo_with_mocks

        result = repo.create_user('test@gmail.com')

        mock_session.assert_called_once()
        db.add.assert_called_once()
        assert result.id == user.id
        assert result.email == user.email

    def test_user_repository_deletes_user(self, user_repo_with_mocks):
        repo, mock_session, db = user_repo_with_mocks

        user_id = str(uuid4())
        result = repo.delete_user(user_id)

        mock_session.assert_called_once()
        db.query.assert_called_once()
        db.query().filter.assert_called_once()
        db.query().filter().delete.assert_called_once()
        assert result == 1

    def test_user_repository_returns_list_of_users(self, user_repo_with_mocks):
        repo, mock_session, db = user_repo_with_mocks

        result = repo.get_all_users()

        mock_session.assert_called_once()
        db.query.assert_called_once()
        db.query().all.assert_called_once_with()

        assert len(result) == 2
        assert isinstance(result[0], User)
        assert isinstance(result[1], User)
