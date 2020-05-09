import mock
import pytest

from app.domain.user import User
from app.request_objects.user import CreateUserRequest
from app.persistence.unit_of_work import SqlAlchemyUnitOfWork
from app.response_objects import ResponseSuccess, ResponseFailure
from app.application.user.commands.create import CreateUserCommand


@pytest.fixture
def create_user_request() -> CreateUserRequest:
    return CreateUserRequest(email='test@gmail.com')


@pytest.fixture
def uow(session_factory) -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(session_factory)


class TestCreateUserCommand:

    def test_create_user_command_executes_correctly(self, create_user_request, uow):
        command = CreateUserCommand(unit_of_work=uow)
        response = command.execute(request=create_user_request)

        user_id = response.value.id
        with uow:
            user = uow.users.get(user_id)

        assert bool(response) is True
        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_RESOURCE_CREATED
        assert response.value.email == 'test@gmail.com'

        assert user.id == user_id
        assert user.email == 'test@gmail.com'
        assert user.courses == []

    def test_create_user_command_returns_exception(self, create_user_request, uow):
        with uow:
            uow.users.add(User(email='test@gmail.com'))

        command = CreateUserCommand(unit_of_work=uow)
        response = command.execute(request=create_user_request)

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'UserAlreadyExists: User with "test@gmail.com" email already exists'

    @mock.patch('app.persistence.unit_of_work.SqlAlchemyUnitOfWork')
    def test_create_user_command_returns_system_error(self, mock_uow, create_user_request):
        session = mock.Mock()
        session.users.add.side_effect = Exception('System error.')
        mock_uow.__enter__.return_value = session

        command = CreateUserCommand(unit_of_work=mock_uow)
        response = command.execute(request=create_user_request)

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.SYSTEM_ERROR
        assert response.message == 'Exception: System error.'
