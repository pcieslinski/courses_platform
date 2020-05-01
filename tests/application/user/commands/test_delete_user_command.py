import pytest
from mock import Mock
from typing import Tuple

from app.request_objects.user import DeleteUserRequest
from app.response_objects import ResponseSuccess, ResponseFailure
from app.application.interfaces.icommand_query import ICommandQuery
from app.application.user.commands.delete import DeleteUserCommand


@pytest.fixture
def delete_user_request() -> DeleteUserRequest:
    return DeleteUserRequest(user_id='123')


@pytest.fixture(scope='function')
def delete_command_with_mocks(
        mock_session_with_db: Tuple[Mock, Mock]) -> Tuple[ICommandQuery, Mock, Mock]:
    session, db = mock_session_with_db
    command = DeleteUserCommand(db_session=session)
    return command, session, db


class TestDeleteUserCommand:

    def test_delete_user_command_initialize_correctly(self):
        session = Mock()
        command = DeleteUserCommand(db_session=session)

        assert isinstance(command, DeleteUserCommand)
        assert hasattr(command, 'db_session')
        assert command.db_session is session

    def test_delete_user_command_executes_correctly(self, delete_user_request,
                                                    delete_command_with_mocks):
        command, mock_session, db = delete_command_with_mocks

        response = command.execute(request=delete_user_request)

        mock_session.assert_called_once()
        db.delete.assert_called_once()

        assert bool(response) is True
        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_NO_CONTENT
        assert response.value == ''

    def test_delete_user_command_returns_system_error_when_generic_exception_is_raised(self,
                                                                                       delete_user_request,
                                                                                       delete_command_with_mocks):
        command, mock_session, db = delete_command_with_mocks
        db.delete.side_effect = Exception('Some error.')

        response = command.execute(request=delete_user_request)

        mock_session.assert_called_once()
        db.delete.assert_called_once()

        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.SYSTEM_ERROR
        assert response.message == 'Exception: Some error.'

    def test_delete_user_command_returns_resource_error_when_called_with_bad_user_id(self,
                                                                                     delete_user_request,
                                                                                     delete_command_with_mocks):
        command, mock_session, db = delete_command_with_mocks
        db.query.return_value.filter_by.return_value.first.return_value = None

        response = command.execute(request=delete_user_request)

        mock_session.assert_called_once()
        assert db.delete.call_count == 0

        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'NoMatchingUser: No User has been found for a given id: 123'
