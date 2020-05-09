import mock
import pytest

from app.domain.user import User
from app.request_objects.user import GetUserRequest
from app.application.user.queries.get import GetUserQuery
from app.persistence.unit_of_work import SqlAlchemyUnitOfWork
from app.response_objects import ResponseSuccess, ResponseFailure


@pytest.fixture
def get_user_request() -> GetUserRequest:
    return GetUserRequest(user_id='100')


@pytest.fixture
def uow(session_factory) -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(session_factory)


class TestGetUserQuery:

    def test_get_user_query_executes_correctly(self, get_user_request, uow):
        with uow:
            uow.users.add(User(id='100', email='test@gmail.com'))

        query = GetUserQuery(unit_of_work=uow)
        response = query.execute(request=get_user_request)

        assert bool(response) is True
        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_OK
        assert response.value.email == 'test@gmail.com'
        assert response.value.courses == []

    def test_qet_user_query_returns_exception_when_no_resource_has_been_found(
            self, get_user_request, uow
    ):
        query = GetUserQuery(unit_of_work=uow)
        response = query.execute(request=get_user_request)

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'NoMatchingUser: No User has been found for a given id: 100'

    @mock.patch('app.persistence.unit_of_work.SqlAlchemyUnitOfWork')
    def test_get_user_query_returns_system_error_when_generic_exception_is_raised(
            self, mock_uow, get_user_request
    ):
        session = mock.Mock()
        session.users.get.side_effect = Exception('System error.')
        mock_uow.__enter__.return_value = session

        query = GetUserQuery(unit_of_work=mock_uow)
        response = query.execute(request=get_user_request)

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.SYSTEM_ERROR
        assert response.message == 'Exception: System error.'
