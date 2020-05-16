import json
import pytest

from app.domain.user import User
from app.domain.course import Course
from app.serializers.schemas import UserSchema, CourseSchema
from app.serializers import (
    user_serializer, users_serializer, course_serializer, courses_serializer
)


@pytest.fixture
def users():
    return [
        User(id='1', email='test@gmail.com'),
        User(id='2', email='dev@gmail.com',
             courses=[
                 Course(id='1', name='Test Course')
             ])
    ]


@pytest.fixture
def courses():
    return [
        Course(id='1', name='Test Course'),
        Course(id='2', name='Sample Course',
               enrollments=[
                   User(id='1', email='test@gmail.com')
               ])
    ]


def test_user_serializer_serializes_correctly_user_domain_model():
    user = User(id='1', email='test@gmail.com')

    serialized_user = user_serializer.dumps(user)

    expected = dict(
        id='1',
        email='test@gmail.com',
    )

    assert json.loads(serialized_user) == expected


def test_users_serializer_serializes_correctly_multiple_user_domain_models(users):
    serialized_users = users_serializer.dumps(users)

    expected = [
        dict(id='1', email='test@gmail.com'),
        dict(id='2', email='dev@gmail.com')
    ]

    assert json.loads(serialized_users) == expected


def test_users_serializer_can_include_courses_while_serializing_domain_model(users):
    users_serializer = UserSchema(many=True, include=['courses'])
    serialized_users = users_serializer.dumps(users)

    expected = [
        dict(id='1', email='test@gmail.com', courses=[]),
        dict(id='2', email='dev@gmail.com', courses=[
            dict(id='1', name='Test Course')
        ])
    ]

    assert json.loads(serialized_users) == expected


def test_course_serializer_serializes_correctly_course_domain_model():
    course = Course(id='1', name='Test Course')

    serialized_course = course_serializer.dumps(course)

    expected = dict(
        id='1',
        name='Test Course'
    )

    assert json.loads(serialized_course) == expected


def test_courses_serializer_serializes_correctly_multiple_course_domain_models(courses):
    serialized_courses = courses_serializer.dumps(courses)

    expected = [
        dict(id='1', name='Test Course'),
        dict(id='2', name='Sample Course')
    ]

    assert json.loads(serialized_courses) == expected


def test_courses_serializer_can_include_enrollments_and_enrollments_count(courses):
    courses_serializer = CourseSchema(
        many=True,
        include=[
            'enrollments',
            'enrollments_count'
        ]
    )
    serialized_courses = courses_serializer.dumps(courses)

    expected = [
        dict(id='1', name='Test Course', enrollments=[], enrollments_count=0),
        dict(id='2', name='Sample Course', enrollments=[
            dict(id='1', email='test@gmail.com')],
             enrollments_count=1)
    ]

    assert json.loads(serialized_courses) == expected
