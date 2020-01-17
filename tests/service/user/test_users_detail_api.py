import mock
from uuid import uuid4

from courses_platform.response_objects import ResponseSuccess


class TestUsersDetailApi:

    @mock.patch('courses_platform.application.user.commands.delete.DeleteUserCommand')
    def test_users_detail_api_deletes_existing_user(self, mock_command, client):
        mock_command().execute.return_value = ResponseSuccess(value='')

        user_id = str(uuid4())
        http_response = client.delete(f'/api/users/{user_id}')

        mock_command().execute.assert_called()
        assert http_response.data == b'""'
        assert http_response.status_code == 200
