import pytest
from mock import Mock
from typing import Any, Dict, List, Union

from app.domain.user import User
from app.domain.course import Course


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


@pytest.fixture
def courses() -> List[Course]:
    course_1 = Course('Test Course')
    course_2 = Course('Sample Course')

    return [
        course_1,
        course_2
    ]


@pytest.fixture
def courses_with_enrollments() -> List[Dict[str, Union[Course, int]]]:
    return [
            {
                'course': Course('Test Course'),
                'enrollments': 10
            }
        ]


@pytest.fixture(scope='function')
def mock_user_repo(user: User, users: List[User]) -> Mock:
    repo = Mock()

    repo.create_user.return_value = user
    repo.delete_user.return_value = 1

    repo.get_user.return_value = user
    repo.get_all_users.return_value = users

    return repo


@pytest.fixture(scope='function')
def mock_course_repo(course: Course, courses: List[Course]) -> Mock:
    repo = Mock()

    repo.create_course.return_value = course
    repo.delete_course.return_value = 1

    repo.get_course.return_value = course
    repo.get_all_courses.return_value = courses

    return repo
