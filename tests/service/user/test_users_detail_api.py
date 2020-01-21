import json
import mock
from uuid import uuid4

from app.response_objects import ResponseSuccess
from app.serializers.json_user_serializer import UserJsonEncoder


class TestUsersDetailApi:

    @mock.patch('app.application.user.queries.get.GetUserQuery')
    def test_users_detail_api_returns_user(self, mock_command, user, client):
        response = ResponseSuccess.build_response_success(user)
        mock_command().execute.return_value = response

        http_response = client.get('/api/users/100')
        user_data = json.dumps(user, cls=UserJsonEncoder)

        _, kwargs = mock_command().execute.call_args

        mock_command().execute.assert_called()
        assert kwargs['request'].user_id == '100'
        assert json.loads(http_response.data) == json.loads(user_data)
        assert http_response.status_code == 200

    @mock.patch('app.application.user.commands.delete.DeleteUserCommand')
    def test_users_detail_api_deletes_existing_user(self, mock_command, client):
        response = ResponseSuccess.build_response_no_content()
        mock_command().execute.return_value = response

        user_id = str(uuid4())
        http_response = client.delete(f'/api/users/{user_id}')

        _, kwargs = mock_command().execute.call_args

        mock_command().execute.assert_called()
        assert kwargs['request'].user_id == user_id
        assert http_response.data == b''
        assert http_response.status_code == 204
