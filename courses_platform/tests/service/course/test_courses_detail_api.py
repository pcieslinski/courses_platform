import json
import mock
from uuid import uuid4

from app.domain.user import User
from app.domain.course import Course
from app.response_objects import ResponseSuccess
from tests.helpers import generate_course_links, generate_user_links


class TestCoursesDetailApi:

    @mock.patch('app.application.course.queries.get.GetCourseQuery')
    def test_courses_detail_api_returns_course(self, mock_query, client):
        course = Course(id='123', name='Test Course')
        response = ResponseSuccess.build_response_success(course)
        mock_query().execute.return_value = response

        http_response = client.get('/api/courses/123')
        expected = dict(
                id='123',
                name='Test Course',
                enrollments_count=0,
                _links=generate_course_links(course_id='123')
            )

        _, kwargs = mock_query().execute.call_args

        mock_query().execute.assert_called()
        assert kwargs['course_id'] == '123'
        assert json.loads(http_response.data) == expected
        assert http_response.status_code == 200

    @mock.patch('app.application.course.queries.get.GetCourseQuery')
    def test_course_detail_api_return_course_with_enrollments(self, mock_query, client):
        course = Course(id='123', name='Test Course', enrollments=[
            User(id='1', email='test@gmail.com')
        ])

        response = ResponseSuccess.build_response_success(course)
        mock_query().execute.return_value = response

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

        _, kwargs = mock_query().execute.call_args
        mock_query().execute.assert_called()
        assert kwargs['course_id'] == '123'
        assert json.loads(http_response.data) == expected
        assert http_response.status_code == 200

    @mock.patch('app.application.course.commands.delete.DeleteCourseCommand')
    def test_courses_detail_api_deletes_existing_course(self, mock_command, client):
        response = ResponseSuccess.build_response_no_content()
        mock_command().execute.return_value = response

        course_id = str(uuid4())
        http_response = client.delete(f'/api/courses/{course_id}')

        _, kwargs = mock_command().execute.call_args

        mock_command().execute.assert_called()
        assert kwargs['course_id'] == course_id
        assert http_response.data == b''
        assert http_response.status_code == 204
