import pytest
from mock import Mock
from typing import Tuple

from app.request_objects import Request
from app.request_objects.user import CreateUserRequest
from app.response_objects import ResponseSuccess, ResponseFailure
from app.application.interfaces.icommand_query import CommandQuery
from app.application.user.commands.create import CreateUserCommand


@pytest.fixture
def create_user_request() -> Request:
    return CreateUserRequest(email='test@gmail.com')


@pytest.fixture(scope='function')
def create_command_with_mocks(
        mock_session_with_db: Tuple[Mock, Mock]) -> Tuple[CommandQuery, Mock, Mock]:
    session, db = mock_session_with_db
    command = CreateUserCommand(db_session=session)
    return command, session, db


class TestCreateUserCommand:

    def test_create_user_command_initialize_correctly(self):
        session = Mock()
        command = CreateUserCommand(db_session=session)

        assert isinstance(command, CreateUserCommand)
        assert hasattr(command, 'db_session')
        assert command.db_session is session

    def test_create_user_command_executes_correctly(self, create_user_request,
                                                    create_command_with_mocks):
        command, mock_session, db = create_command_with_mocks

        response = command.execute(request=create_user_request)

        mock_session.assert_called_once()
        db.add.assert_called_once()

        assert bool(response) is True
        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_RESOURCE_CREATED
        assert not hasattr(response.value, 'courses')
        assert response.value.email == 'test@gmail.com'

    def test_create_user_command_returns_exception(self, create_user_request,
                                                   create_command_with_mocks):
        command, mock_session, db = create_command_with_mocks
        db.add.side_effect = Exception(
            'User with test@gmail.com email already exists.'
        )

        response = command.execute(request=create_user_request)

        mock_session.assert_called_once()
        db.add.assert_called_once()

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'Exception: User with test@gmail.com email already exists.'
