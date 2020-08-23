import mock

from app.domain.user import User
from app.application.user import commands
from app.response_objects import ResponseSuccess, ResponseFailure


class TestCreateUserCommand:

    def test_create_user_command_executes_correctly(self, uow):
        command = commands.CreateUserCommand(unit_of_work=uow)
        response = command.execute(email='test@gmail.com')

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

    def test_create_user_command_returns_exception(self, uow):
        with uow:
            uow.users.add(User(email='test@gmail.com'))

        command = commands.CreateUserCommand(unit_of_work=uow)
        response = command.execute(email='test@gmail.com')

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'UserAlreadyExists: User with "test@gmail.com" email already exists'

    @mock.patch('app.adapters.unit_of_work.SqlAlchemyUnitOfWork')
    def test_create_user_command_returns_system_error(self, mock_uow):
        session = mock.Mock()
        session.users.add.side_effect = Exception('System error.')
        mock_uow.__enter__.return_value = session

        command = commands.CreateUserCommand(unit_of_work=mock_uow)
        response = command.execute(email='test@gmail.com')

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.SYSTEM_ERROR
        assert response.message == 'Exception: System error.'


class TestDeleteUserCommand:

    def test_delete_user_command_executes_correctly(self, uow):
        with uow:
            uow.users.add(User(id='123', email='test@gmail.com'))

        command = commands.DeleteUserCommand(unit_of_work=uow)
        response = command.execute(user_id='123')

        with uow:
            user = uow.users.get('123')

        assert bool(response) is True
        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_NO_CONTENT
        assert response.value == ''
        assert user is None

    @mock.patch('app.adapters.unit_of_work.SqlAlchemyUnitOfWork')
    def test_delete_user_command_returns_system_error_when_generic_exception_is_raised(self, mock_uow):
        session = mock.Mock()
        session.users.remove.side_effect = Exception('Some error.')
        mock_uow.__enter__.return_value = session

        command = commands.DeleteUserCommand(unit_of_work=mock_uow)
        response = command.execute(user_id='123')

        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.SYSTEM_ERROR
        assert response.message == 'Exception: Some error.'

    def test_delete_user_command_returns_resource_error_when_called_with_bad_user_id(self, uow):
        command = commands.DeleteUserCommand(unit_of_work=uow)
        response = command.execute(user_id='123')

        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'NoMatchingUser: No User has been found for a given id: 123'
