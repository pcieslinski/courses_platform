import mock
from uuid import uuid4

from app.response_objects import ResponseSuccess


class TestUsersDetailApi:

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
