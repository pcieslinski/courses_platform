import pytest
from mock import Mock
from uuid import uuid4
from typing import Tuple

from courses_platform.application.interfaces.icommand_query import CommandQuery
from courses_platform.application.user.commands.delete import DeleteUserCommand, NoMatchingUser


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

    def test_delete_user_command_executes_correctly(self, user, delete_command_with_mock_repo):
        user_id = user.id
        command, repo = delete_command_with_mock_repo

        result = command.execute(user_id=user_id)

        repo.delete_user.assert_called_with(user_id=user_id)
        assert result

    def test_delete_user_command_returns_exception_when_called_with_bad_user_id(self):
        user_id = str(uuid4())

        repo = Mock()
        repo.delete_user.side_effect = NoMatchingUser(f'No match for User with id {user_id}.')
        command = DeleteUserCommand(repo=repo)

        with pytest.raises(NoMatchingUser) as exc:
            result = command.execute(user_id=user_id)

            repo.delete_user.assert_called_with(user_id=user_id)
            assert str(exc) == f'No match for User with id {user_id}.'
