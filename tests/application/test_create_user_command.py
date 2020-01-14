import pytest

from courses_platform.application.user.commands.create import CreateUserCommand


@pytest.fixture(scope='function')
def create_command_with_mock_repo(mock_user_repo):
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
