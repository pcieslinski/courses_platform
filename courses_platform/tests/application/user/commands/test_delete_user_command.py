import mock
import pytest

from app.domain.user import User
from app.request_objects.user import DeleteUserRequest
from app.persistence.unit_of_work import SqlAlchemyUnitOfWork
from app.response_objects import ResponseSuccess, ResponseFailure
from app.application.user.commands.delete import DeleteUserCommand


@pytest.fixture
def delete_user_request() -> DeleteUserRequest:
    return DeleteUserRequest(user_id='123')


@pytest.fixture
def uow(session_factory) -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(session_factory)


class TestDeleteUserCommand:

    def test_delete_user_command_executes_correctly(self, delete_user_request, uow):
        with uow:
            uow.users.add(User(id='123', email='test@gmail.com'))

        command = DeleteUserCommand(unit_of_work=uow)
        response = command.execute(request=delete_user_request)

        with uow:
            user = uow.users.get('123')

        assert bool(response) is True
        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_NO_CONTENT
        assert response.value == ''
        assert user is None

    @mock.patch('app.persistence.unit_of_work.SqlAlchemyUnitOfWork')
    def test_delete_user_command_returns_system_error_when_generic_exception_is_raised(
            self, mock_uow, delete_user_request
    ):
        session = mock.Mock()
        session.users.remove.side_effect = Exception('Some error.')
        mock_uow.__enter__.return_value = session

        command = DeleteUserCommand(unit_of_work=mock_uow)
        response = command.execute(request=delete_user_request)

        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.SYSTEM_ERROR
        assert response.message == 'Exception: Some error.'

    def test_delete_user_command_returns_resource_error_when_called_with_bad_user_id(
            self, delete_user_request, uow
    ):
        command = DeleteUserCommand(unit_of_work=uow)
        response = command.execute(request=delete_user_request)

        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'NoMatchingUser: No User has been found for a given id: 123'
