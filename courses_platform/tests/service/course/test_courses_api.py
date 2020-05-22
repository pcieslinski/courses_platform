import json
from typing import List

import mock
import pytest

from app.domain.user import User
from app.domain.course import Course
from app.response_objects import ResponseSuccess
from app.serializers import course_serializer, courses_serializer


@pytest.fixture
def courses_with_enrollments() -> List[Course]:
    return [
        Course(id='1', name='Test Course', enrollments=[
            User(id='2', email='test@gmail.com')
        ])
    ]


class TestCoursesApi:

    @mock.patch('app.application.course.queries.get_all.GetAllCoursesQuery')
    def test_courses_api_returns_list_of_courses(self, mock_query, client):
        response_val = [Course('Test Course')]
        response = ResponseSuccess.build_response_success(response_val)
        mock_query().execute.return_value = response

        http_response = client.get('/api/courses')
        courses_data = courses_serializer.dumps(response_val)

        assert json.loads(http_response.data.decode('UTF-8')) == json.loads(courses_data)
        assert mock_query().execute.call_count == 1
        assert http_response.status_code == 200
        assert http_response.mimetype == 'application/json'

    @mock.patch('app.application.course.queries.get_all.GetAllCoursesQuery')
    def test_courses_api_returns_list_of_courses_with_enrollments_count(
            self, mock_query, client, courses_with_enrollments
    ):
        response = ResponseSuccess.build_response_success(courses_with_enrollments)
        mock_query().execute.return_value = response

        http_response = client.get('/api/courses?include=enrollments_count')

        expected = [
            dict(
                id='1',
                name='Test Course',
                enrollments_count=1
            )
        ]

        assert json.loads(http_response.data.decode('UTF-8')) == expected
        assert mock_query().execute.call_count == 1
        assert http_response.status_code == 200
        assert http_response.mimetype == 'application/json'

    @mock.patch('app.application.course.queries.get_all.GetAllCoursesQuery')
    def test_courses_api_returns_list_of_courses_with_enrollments(
            self, mock_query, client, courses_with_enrollments
    ):
        response = ResponseSuccess.build_response_success(courses_with_enrollments)
        mock_query().execute.return_value = response

        http_response = client.get('/api/courses?include=enrollments')

        expected = [
            dict(
                id='1',
                name='Test Course',
                enrollments=[
                    dict(id='2', email='test@gmail.com')
                ]
            )
        ]

        assert json.loads(http_response.data.decode('UTF-8')) == expected
        assert mock_query().execute.call_count == 1
        assert http_response.status_code == 200
        assert http_response.mimetype == 'application/json'

    @mock.patch('app.application.course.commands.create.CreateCourseCommand')
    def test_courses_api_creates_new_course(self, mock_command, client, course):
        response = ResponseSuccess.build_response_resource_created(course)
        mock_command().execute.return_value = response

        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype
        }

        data = json.dumps(dict(name='Test Course'))

        http_response = client.post('/api/courses', data=data, headers=headers)
        course_data = course_serializer.dumps(course)

        _, kwargs = mock_command().execute.call_args

        assert json.loads(http_response.data.decode('UTF-8')) == json.loads(course_data)
        mock_command().execute.assert_called()
        assert kwargs['name'] == 'Test Course'
        assert http_response.status_code == 201
        assert http_response.mimetype == 'application/json'
