import pytest
from typing import Dict, List, Union

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
