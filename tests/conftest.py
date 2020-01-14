import pytest
from mock import Mock
from typing import List

from courses_platform.domain.user import User
from courses_platform.domain.course import Course


@pytest.fixture
def user() -> User:
    return User('test@gmail.com')


@pytest.fixture
def course() -> Course:
    return Course(name='Test Course')


@pytest.fixture
def users() -> List[User]:
    user_1 = User('test@gmail.com')
    user_2 = User('sample@gmail.com')

    return [
        user_1,
        user_2
    ]


@pytest.fixture(scope='function')
def mock_user_repo(user: User, users: List[User]) -> Mock:
    repo = Mock()

    repo.create_user.return_value = user
    repo.delete_user.return_value = user

    repo.get_all_users.return_value = users

    return repo


@pytest.fixture(scope='function')
def mock_course_repo(course: Course) -> Mock:
    repo = Mock()

    repo.create_course.return_value = course
    repo.delete_course.return_value = course

    return repo

