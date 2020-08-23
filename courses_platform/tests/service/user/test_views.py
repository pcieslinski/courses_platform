import json
import mock
from uuid import uuid4

from app.domain.user import User
from app.domain.course import Course
from app.application.user import queries
from app.application.user import commands
from app.response_objects import ResponseSuccess
from tests.helpers import generate_user_links, generate_course_links


class TestUsersApi:

    @mock.patch.object(queries.GetAllUsersQuery, 'execute')
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

    @mock.patch.object(queries.GetAllUsersQuery, 'execute')
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

    @mock.patch.object(commands.CreateUserCommand, 'execute')
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


class TestUsersCoursesApi:

    @mock.patch.object(queries.GetUserCoursesQuery, 'execute')
    def test_users_courses_api_returns_list_of_user_courses(self, mock_query, client):
        response_val = [Course(id='1', name='Test Course')]
        response = ResponseSuccess.build_response_success(response_val)
        mock_query.return_value = response

        http_response = client.get('/api/users/123/courses')
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


class TestUsersDetailApi:

    @mock.patch.object(queries.GetUserQuery, 'execute')
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

    @mock.patch.object(queries.GetUserQuery, 'execute')
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

    @mock.patch.object(commands.DeleteUserCommand, 'execute')
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
