import json
import mock

from app.domain.user import User
from app.domain.course import Course
from app.response_objects import ResponseSuccess
from app.application.user.queries import GetAllUsersQuery
from app.application.user.commands import CreateUserCommand
from tests.helpers import generate_user_links, generate_course_links


class TestUsersApi:

    @mock.patch.object(GetAllUsersQuery, 'execute')
    def test_users_api_returns_list_of_users(self, mock_query, client):
        response_val = [User(id='1', email='test@gmail.com')]
        response = ResponseSuccess.build_response_success(response_val)
        mock_query.return_value = response

        http_response = client.get('/api/users')
        expected = [
            dict(
                id='1',
                email='test@gmail.com',
                _links=generate_user_links(user_id='1')
            )
        ]

        assert json.loads(http_response.data.decode('UTF-8')) == expected
        mock_query.assert_called_with()
        assert http_response.status_code == 200
        assert http_response.mimetype == 'application/json'

    @mock.patch.object(GetAllUsersQuery, 'execute')
    def test_users_api_returns_list_of_users_with_courses(self, mock_query, client):
        response_val = [
            User(id='1', email='test@gmail.com', courses=[
                Course(id='2', name='Test Course')
            ])
        ]

        response = ResponseSuccess.build_response_success(response_val)
        mock_query.return_value = response

        http_response = client.get('/api/users?include=courses')

        expected = [
            dict(
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
        ]

        assert json.loads(http_response.data.decode('UTF-8')) == expected
        mock_query.assert_called_with()
        assert http_response.status_code == 200
        assert http_response.mimetype == 'application/json'

    @mock.patch.object(CreateUserCommand, 'execute')
    def test_users_api_creates_new_user(self, mock_command, client):
        user = User(id='1', email='test@gmail.com')
        response = ResponseSuccess.build_response_resource_created(user)
        mock_command.return_value = response

        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype
        }
        data = json.dumps(dict(email='test@gmail.com'))

        http_response = client.post('/api/users', data=data, headers=headers)
        expected = dict(
                id='1',
                email='test@gmail.com',
                _links=generate_user_links(user_id='1')
            )

        _, kwargs = mock_command.call_args

        assert json.loads(http_response.data.decode('UTF-8')) == expected
        mock_command.assert_called()
        assert kwargs['email'] == 'test@gmail.com'
        assert http_response.status_code == 201
        assert http_response.mimetype == 'application/json'
