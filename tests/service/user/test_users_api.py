import json
import mock

from courses_platform.response_objects import ResponseSuccess
from courses_platform.serializers.json_user_serializer import UserJsonEncoder


class TestUsersApi:

    @mock.patch('courses_platform.application.user.queries.get_all.GetAllUsersQuery')
    def test_users_api_returns_list_of_users(self, mock_query, client, users):
        response = ResponseSuccess.build_response_success(users)
        mock_query().execute.return_value = response

        http_response = client.get('/api/users')
        users_data = json.dumps(users, cls=UserJsonEncoder)

        assert json.loads(http_response.data.decode('UTF-8')) == json.loads(users_data)
        mock_query().execute.assert_called_with()
        assert http_response.status_code == 200
        assert http_response.mimetype == 'application/json'

    @mock.patch('courses_platform.application.user.queries.get_all.GetAllUsersQuery')
    def test_users_api_returns_empty_list_of_users(self, mock_query, client):
        response = ResponseSuccess.build_response_success([])
        mock_query().execute.return_value = response

        http_response = client.get('/api/users')

        assert json.loads(http_response.data.decode('UTF-8')) == []
        mock_query().execute.assert_called_with()
        assert http_response.status_code == 200
        assert http_response.mimetype == 'application/json'

    @mock.patch('courses_platform.application.user.commands.create.CreateUserCommand')
    def test_users_api_creates_new_user(self, mock_command, client, user):
        response = ResponseSuccess.build_response_resource_created(user)
        mock_command().execute.return_value = response

        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype
        }
        data = json.dumps(dict(email='test@gmail.com'))

        http_response = client.post('/api/users', data=data, headers=headers)
        user_data = json.dumps(user, cls=UserJsonEncoder)

        _, kwargs = mock_command().execute.call_args

        assert json.loads(http_response.data.decode('UTF-8')) == json.loads(user_data)
        mock_command().execute.assert_called()
        assert kwargs['request'].email == 'test@gmail.com'
        assert http_response.status_code == 201
        assert http_response.mimetype == 'application/json'
