import json
import mock

from app.domain.user import User
from tests.helpers import generate_user_links
from app.response_objects import ResponseSuccess


class TestUsersApi:

    @mock.patch('app.application.user.queries.get_all.GetAllUsersQuery')
    def test_users_api_returns_list_of_users(self, mock_query, client):
        response_val = [User(id='1', email='test@gmail.com')]
        response = ResponseSuccess.build_response_success(response_val)
        mock_query().execute.return_value = response

        http_response = client.get('/api/users')
        expected = [
            dict(
                id='1',
                email='test@gmail.com',
                _links=generate_user_links(user_id='1')
            )
        ]

        assert json.loads(http_response.data.decode('UTF-8')) == expected
        mock_query().execute.assert_called_with()
        assert http_response.status_code == 200
        assert http_response.mimetype == 'application/json'

    @mock.patch('app.application.user.commands.create.CreateUserCommand')
    def test_users_api_creates_new_user(self, mock_command, client):
        user = User(id='1', email='test@gmail.com')
        response = ResponseSuccess.build_response_resource_created(user)
        mock_command().execute.return_value = response

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

        _, kwargs = mock_command().execute.call_args

        assert json.loads(http_response.data.decode('UTF-8')) == expected
        mock_command().execute.assert_called()
        assert kwargs['email'] == 'test@gmail.com'
        assert http_response.status_code == 201
        assert http_response.mimetype == 'application/json'
