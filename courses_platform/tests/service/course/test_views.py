import json
from uuid import uuid4
from typing import List


import mock
import pytest

from app.domain.user import User
from app.domain.course import Course
from app.application.course import queries
from app.application.course import commands
from app.response_objects import ResponseSuccess
from tests.helpers import generate_user_links, generate_course_links


@pytest.fixture
def courses_with_enrollments() -> List[Course]:
    return [
        Course(id='1', name='Test Course', enrollments=[
            User(id='2', email='test@gmail.com')
        ])
    ]


class TestCoursesApi:

    @mock.patch.object(queries.GetAllCoursesQuery, 'execute')
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

    @mock.patch.object(queries.GetAllCoursesQuery, 'execute')
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

    @mock.patch.object(commands.CreateCourseCommand, 'execute')
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


class TestCoursesDetailApi:

    @mock.patch.object(queries.GetCourseQuery, 'execute')
    def test_courses_detail_api_returns_course(self, mock_query, client):
        course = Course(id='123', name='Test Course')
        response = ResponseSuccess.build_response_success(course)
        mock_query.return_value = response

        http_response = client.get('/api/courses/123')
        expected = dict(
                id='123',
                name='Test Course',
                enrollments_count=0,
                _links=generate_course_links(course_id='123')
            )

        _, kwargs = mock_query.call_args

        mock_query.assert_called()
        assert kwargs['course_id'] == '123'
        assert json.loads(http_response.data) == expected
        assert http_response.status_code == 200

    @mock.patch.object(queries.GetCourseQuery, 'execute')
    def test_course_detail_api_return_course_with_enrollments(self, mock_query, client):
        course = Course(id='123', name='Test Course', enrollments=[
            User(id='1', email='test@gmail.com')
        ])

        response = ResponseSuccess.build_response_success(course)
        mock_query.return_value = response

        http_response = client.get('/api/courses/123?include=enrollments')

        expected = dict(
                id='123',
                name='Test Course',
                enrollments_count=1,
                _links=generate_course_links(course_id='123'),
                enrollments=[
                    dict(
                        id='1',
                        email='test@gmail.com',
                        _links=generate_user_links(user_id='1')
                    )
                ]
            )

        _, kwargs = mock_query.call_args
        mock_query.assert_called()
        assert kwargs['course_id'] == '123'
        assert json.loads(http_response.data) == expected
        assert http_response.status_code == 200

    @mock.patch.object(commands.DeleteCourseCommand, 'execute')
    def test_courses_detail_api_deletes_existing_course(self, mock_command, client):
        response = ResponseSuccess.build_response_no_content()
        mock_command.return_value = response

        course_id = str(uuid4())
        http_response = client.delete(f'/api/courses/{course_id}')

        _, kwargs = mock_command.call_args

        mock_command.assert_called()
        assert kwargs['course_id'] == course_id
        assert http_response.data == b''
        assert http_response.status_code == 204


class TestEnrollmentsApi:

    @mock.patch.object(commands.EnrollUserCommand, 'execute')
    def test_enrollments_api_enrolls_user_for_course(self, mock_command, client):
        request_data = dict(course_id='123', user_id='1')
        response = ResponseSuccess.build_response_resource_created(request_data)
        mock_command.return_value = response

        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype
        }

        data = json.dumps(dict(user_id='1'))

        http_response = client.post('/api/courses/123/users', data=data, headers=headers)

        _, kwargs = mock_command.call_args

        assert json.loads(http_response.data.decode('UTF-8')) == request_data
        mock_command.assert_called()
        assert kwargs['course_id'] == '123'
        assert kwargs['user_id'] == '1'
        assert http_response.status_code == 201
        assert http_response.mimetype == 'application/json'


class TestEnrollmentsDetailApi:

    @mock.patch.object(commands.WithdrawUserEnrollmentCommand, 'execute')
    def test_enrollments_detail_api_withdraws_user_enrollment(self, mock_command, client):
        response = ResponseSuccess.build_response_no_content()
        mock_command.return_value = response

        http_response = client.delete('/api/courses/123/users/20')

        _, kwargs = mock_command.call_args

        mock_command.assert_called()
        assert kwargs['course_id'] == '123'
        assert kwargs['user_id'] == '20'
        assert http_response.data == b''
        assert http_response.status_code == 204
