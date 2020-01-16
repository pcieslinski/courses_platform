import pytest
from uuid import uuid4
from mock import Mock, patch

from courses_platform.domain.user import User
from courses_platform.persistence.repositories.user.user_repository import UserRepository


@pytest.fixture
def user_record():
    return {
        'id': str(uuid4()),
        'email': 'test@gmail.com'
    }


class TestUserRepository:

    def test_user_repository_initialize_correctly(self):
        session = Mock()
        repo = UserRepository(db_session=session)

        assert isinstance(repo, UserRepository)
        assert hasattr(repo, 'db_session')
        assert repo.db_session is session

    @patch('uuid.UUID')
    @patch('courses_platform.persistence.database.session', autospec=True)
    def test_user_repository_creates_user(self, mock_session, mock_uuid, user_record):
        user = User.from_record(user_record)

        db = Mock()
        mock_session.return_value.__enter__.return_value = db
        mock_uuid.return_value = user.id

        repo = UserRepository(db_session=mock_session)
        result = repo.create_user('test@gmail.com')

        db.add.assert_called_once()
        assert result.id == user.id
        assert result.email == user.email
