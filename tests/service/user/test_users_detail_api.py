import mock
from uuid import uuid4

from courses_platform.application.user.commands.delete import NoMatchingUser


class TestUsersDetailApi:

    @mock.patch('courses_platform.application.user.commands.delete.DeleteUserCommand')
    def test_users_detail_api_deletes_existing_user(self, mock_command, client):
        mock_command().execute.return_value = 1

        user_id = str(uuid4())
        http_response = client.delete(f'/api/users/{user_id}')

        mock_command().execute.assert_called_with(user_id)
        assert http_response.json is None
        assert http_response.status_code == 204

    @mock.patch('courses_platform.application.user.commands.delete.DeleteUserCommand')
    def test_users_detail_api_raises_error_when_deletes_not_existing_user(self, mock_command, client):
        mock_command().execute.side_effect = NoMatchingUser

        http_response = client.delete('/api/users/bad_id')

        mock_command().execute.assert_called_with('bad_id')
        assert http_response.json['message'] == 'No User has been found for a given id: bad_id'
        assert http_response.status_code == 404
        assert http_response.mimetype == 'application/json'
