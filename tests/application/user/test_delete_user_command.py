import pytest
from mock import Mock
from typing import Tuple

from courses_platform.request_objects import Request
from courses_platform.request_objects.user import DeleteUserRequest
from courses_platform.response_objects import ResponseSuccess, ResponseFailure
from courses_platform.application.interfaces.icommand_query import CommandQuery
from courses_platform.application.user.commands.delete import DeleteUserCommand


@pytest.fixture
def delete_user_request() -> Request:
    return DeleteUserRequest(user_id='123')


@pytest.fixture(scope='function')
def delete_command_with_mock_repo(mock_user_repo: Mock) -> Tuple[CommandQuery, Mock]:
    command = DeleteUserCommand(repo=mock_user_repo)
    return command, mock_user_repo


class TestDeleteUserCommand:

    def test_delete_user_command_initialize_correctly(self, delete_command_with_mock_repo):
        command, repo = delete_command_with_mock_repo

        assert isinstance(command, DeleteUserCommand)
        assert hasattr(command, 'repo')
        assert command.repo is repo

    def test_delete_user_command_executes_correctly(self, delete_command_with_mock_repo,
                                                    delete_user_request):
        command, repo = delete_command_with_mock_repo

        response = command.execute(request=delete_user_request)

        repo.delete_user.assert_called_with(user_id='123')
        assert bool(response) is True
        assert isinstance(response, ResponseSuccess)
        assert response.value is ''

    def test_delete_user_command_returns_exception_when_called_with_bad_user_id(self,
                                                                                delete_user_request):
        repo = Mock()
        repo.delete_user.side_effect = Exception(f'No match for User with id 123.')
        command = DeleteUserCommand(repo=repo)

        response = command.execute(request=delete_user_request)

        repo.delete_user.assert_called_with(user_id='123')
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'Exception: No match for User with id 123.'

