import pytest
from mock import Mock
from typing import Tuple

from courses_platform.request_objects import Request
from courses_platform.request_objects.user import CreateUserRequest
from courses_platform.response_objects import ResponseSuccess, ResponseFailure
from courses_platform.application.interfaces.icommand_query import CommandQuery
from courses_platform.application.user.commands.create import CreateUserCommand


@pytest.fixture
def create_user_request() -> Request:
    return CreateUserRequest(email='test@gmail.com')


@pytest.fixture(scope='function')
def create_command_with_mock_repo(mock_user_repo: Mock) -> Tuple[CommandQuery, Mock]:
    command = CreateUserCommand(repo=mock_user_repo)
    return command, mock_user_repo


class TestCreateUserCommand:

    def test_create_user_command_initialize_correctly(self, create_command_with_mock_repo):
        command, repo = create_command_with_mock_repo

        assert isinstance(command, CreateUserCommand)
        assert hasattr(command, 'repo')
        assert command.repo is repo

    def test_create_user_command_executes_correctly(self, create_command_with_mock_repo,
                                                    create_user_request):
        command, repo = create_command_with_mock_repo

        response = command.execute(request=create_user_request)

        repo.create_user.assert_called_with(email='test@gmail.com')
        assert bool(response) is True
        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_RESOURCE_CREATED
        assert response.value.email == 'test@gmail.com'

    def test_create_user_command_returns_exception(self, create_user_request):
        repo = Mock()
        repo.create_user.side_effect = Exception(
            'User with test@gmail.com email already exists.'
        )
        command = CreateUserCommand(repo=repo)

        response = command.execute(request=create_user_request)

        repo.create_user.assert_called_with(email='test@gmail.com')
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'Exception: User with test@gmail.com email already exists.'
