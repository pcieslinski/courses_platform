import json
import mock
from uuid import uuid4

from app.domain.user import User
from app.domain.course import Course
from app.response_objects import ResponseSuccess
from app.application.user.queries import GetUserQuery
from app.application.user.commands import DeleteUserCommand
from tests.helpers import generate_user_links, generate_course_links


class TestUsersDetailApi:

    @mock.patch.object(GetUserQuery, 'execute')
    def test_users_detail_api_returns_user(self, mock_query, client):
        user = User(id='1', email='test@gmail.com')
        response = ResponseSuccess.build_response_success(user)
        mock_query.return_value = response

        http_response = client.get('/api/users/100')
        expected = dict(
                id='1',
                email='test@gmail.com',
                _links=generate_user_links(user_id='1')
            )

        _, kwargs = mock_query.call_args

        mock_query.assert_called()
        assert kwargs['user_id'] == '100'
        assert json.loads(http_response.data) == expected
        assert http_response.status_code == 200

    @mock.patch.object(GetUserQuery, 'execute')
    def test_users_detail_api_returns_user_with_courses(self, mock_query, client):
        user = User(id='1', email='test@gmail.com', courses=[
            Course(id='2', name='Test Course')
        ])

        response = ResponseSuccess.build_response_success(user)
        mock_query.return_value = response

        http_response = client.get('/api/users/1?include=courses')

        expected = dict(
            id='1',
            email='test@gmail.com',
            _links=generate_user_links(user_id='1'),
            courses=[
                dict(
                    id='2',
                    name='Test Course',
                    _links=generate_course_links(course_id='2')
                )
            ]

        )

        _, kwargs = mock_query.call_args

        mock_query.assert_called()
        assert kwargs['user_id'] == '1'
        assert json.loads(http_response.data) == expected
        assert http_response.status_code == 200

    @mock.patch.object(DeleteUserCommand, 'execute')
    def test_users_detail_api_deletes_existing_user(self, mock_command, client):
        response = ResponseSuccess.build_response_no_content()
        mock_command.return_value = response

        user_id = str(uuid4())
        http_response = client.delete(f'/api/users/{user_id}')

        _, kwargs = mock_command.call_args

        mock_command.assert_called()
        assert kwargs['user_id'] == user_id
        assert http_response.data == b''
        assert http_response.status_code == 204
