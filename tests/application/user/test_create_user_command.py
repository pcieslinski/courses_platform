import pytest
from mock import Mock
from typing import Tuple

from courses_platform.application.interfaces.icommand_query import CommandQuery
from courses_platform.application.user.commands.create import CreateUserCommand, UserAlreadyExists


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

    def test_create_user_command_executes_correctly(self, create_command_with_mock_repo):
        command, repo = create_command_with_mock_repo

        result = command.execute(email='test@gmail.com')

        repo.create_user.assert_called_with(email='test@gmail.com')
        assert result.email == 'test@gmail.com'

    def test_create_user_command_returns_exception_when_called_with_already_existing_user_email(self):
        repo = Mock()
        repo.create_user.side_effect = UserAlreadyExists(
            'User with test@gmail.com email already exists.'
        )
        command = CreateUserCommand(repo=repo)

        result = command.execute(email='test@gmail.com')

        repo.create_user.assert_called_with(email='test@gmail.com')
        assert isinstance(result, UserAlreadyExists)
        assert str(result) == 'User with test@gmail.com email already exists.'
