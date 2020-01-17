import json
import mock

from courses_platform.serializers.json_user_serializer import UserJsonEncoder


class TestUserApi:

    @mock.patch('courses_platform.application.user.queries.get_all.GetAllUsersQuery')
    def test_user_api_returns_list_of_users(self, mock_query, client, users):
        mock_query().execute.return_value = users

        http_response = client.get('/api/users')
        users_data = json.dumps(users, cls=UserJsonEncoder)

        assert json.loads(http_response.data.decode('UTF-8')) == json.loads(users_data)
        mock_query().execute.assert_called_with()
        assert http_response.status_code == 200
        assert http_response.mimetype == 'application/json'

    @mock.patch('courses_platform.application.user.queries.get_all.GetAllUsersQuery')
    def test_user_api_returns_empty_list_of_users(self, mock_query, client):
        mock_query().execute.return_value = []

        http_response = client.get('/api/users')

        assert json.loads(http_response.data.decode('UTF-8')) == []
        mock_query().execute.assert_called_with()
        assert http_response.status_code == 200
        assert http_response.mimetype == 'application/json'

    @mock.patch('courses_platform.application.user.commands.create.CreateUserCommand')
    def test_user_api_creates_new_user(self, mock_command, client, user):
        mock_command().execute.return_value = user

        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype
        }
        data = json.dumps(dict(email='test@gmail.com'))

        http_response = client.post('/api/users', data=data, headers=headers)
        user_data = json.dumps(user, cls=UserJsonEncoder)

        assert json.loads(http_response.data.decode('UTF-8')) == json.loads(user_data)
        mock_command().execute.assert_called_with('test@gmail.com')
        assert http_response.status_code == 201
        assert http_response.mimetype == 'application/json'
