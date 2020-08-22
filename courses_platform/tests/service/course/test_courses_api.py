import json
from typing import List

import mock
import pytest

from app.domain.user import User
from app.domain.course import Course
from app.response_objects import ResponseSuccess
from app.application.course.queries import GetAllCoursesQuery
from app.application.course.commands import CreateCourseCommand
from tests.helpers import generate_user_links, generate_course_links


@pytest.fixture
def courses_with_enrollments() -> List[Course]:
    return [
        Course(id='1', name='Test Course', enrollments=[
            User(id='2', email='test@gmail.com')
        ])
    ]


class TestCoursesApi:

    @mock.patch.object(GetAllCoursesQuery, 'execute')
    def test_courses_api_returns_list_of_courses(self, mock_query, client):
        response_val = [Course(id='1', name='Test Course')]
        response = ResponseSuccess.build_response_success(response_val)
        mock_query.return_value = response

        http_response = client.get('/api/courses')

        expected = [
            dict(
                id='1',
                name='Test Course',
                enrollments_count=0,
                _links=generate_course_links(course_id='1')
            )
        ]

        assert json.loads(http_response.data.decode('UTF-8')) == expected
        assert mock_query.call_count == 1
        assert http_response.status_code == 200
        assert http_response.mimetype == 'application/json'

    @mock.patch.object(GetAllCoursesQuery, 'execute')
    def test_courses_api_returns_list_of_courses_with_enrollments(
            self, mock_query, client, courses_with_enrollments
    ):
        response = ResponseSuccess.build_response_success(courses_with_enrollments)
        mock_query.return_value = response

        http_response = client.get('/api/courses?include=enrollments')

        expected = [
            dict(
                id='1',
                name='Test Course',
                enrollments_count=1,
                _links=generate_course_links(course_id='1'),
                enrollments=[
                    dict(
                        id='2',
                        email='test@gmail.com',
                        _links=generate_user_links(user_id='2')
                    )
                ]
            )
        ]

        assert json.loads(http_response.data.decode('UTF-8')) == expected
        assert mock_query.call_count == 1
        assert http_response.status_code == 200
        assert http_response.mimetype == 'application/json'

    @mock.patch.object(CreateCourseCommand, 'execute')
    def test_courses_api_creates_new_course(self, mock_command, client):
        course = Course(id='1', name='Test Course')
        response = ResponseSuccess.build_response_resource_created(course)
        mock_command.return_value = response

        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype
        }

        data = json.dumps(dict(name='Test Course'))

        http_response = client.post('/api/courses', data=data, headers=headers)
        expected = dict(
                id='1',
                name='Test Course',
                enrollments_count=0,
                _links=generate_course_links(course_id='1')
            )

        _, kwargs = mock_command.call_args

        assert json.loads(http_response.data.decode('UTF-8')) == expected
        mock_command.assert_called()
        assert kwargs['name'] == 'Test Course'
        assert http_response.status_code == 201
        assert http_response.mimetype == 'application/json'
