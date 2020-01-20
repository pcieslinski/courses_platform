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
def delete_command_with_mocks(
        mock_session_with_db: Tuple[Mock, Mock]) -> Tuple[CommandQuery, Mock, Mock]:
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
        db.query().filter().delete.assert_called_once()

        assert bool(response) is True
        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_NO_CONTENT
        assert response.value is ''

    def test_delete_user_command_returns_system_error_when_generic_exception_is_raised(self,
                                                                                       delete_user_request,
                                                                                       delete_command_with_mocks):
        command, mock_session, db = delete_command_with_mocks
        db.query.return_value.filter.return_value.delete.side_effect = Exception('Some error.')

        response = command.execute(request=delete_user_request)

        mock_session.assert_called_once()
        db.query().filter().delete.assert_called_once()

        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.SYSTEM_ERROR
        assert response.message == 'Exception: Some error.'

    def test_delete_user_command_returns_resource_error_when_called_with_bad_user_id(self,
                                                                                     delete_user_request,
                                                                                     delete_command_with_mocks):
        command, mock_session, db = delete_command_with_mocks
        db.query.return_value.filter.return_value.delete.return_value = 0

        response = command.execute(request=delete_user_request)

        mock_session.assert_called_once()
        db.query().filter().delete.assert_called_once()

        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'NoMatchingUser: No User has been found for a given id: 123'

