import pytest
from mock import Mock

from courses_platform.domain.user import User


@pytest.fixture
def user() -> User:
    return User('test@gmail.com')


@pytest.fixture(scope='function')
def mock_user_repo(user) -> Mock:
    repo = Mock()

    repo.create_user.return_value = user
    repo.delete_user.return_value = user

    return repo
