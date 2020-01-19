import pytest
from mock import Mock
from typing import Tuple

from courses_platform.request_objects import Request
from courses_platform.request_objects.user import GetUserRequest
from courses_platform.response_objects import ResponseSuccess, ResponseFailure
from courses_platform.application.user.queries.get import GetUserQuery
from courses_platform.application.interfaces.icommand_query import CommandQuery


@pytest.fixture
def get_user_request() -> Request:
    return GetUserRequest(user_id='100')


@pytest.fixture(scope='function')
def get_query_with_mocks(
        mock_session_with_db: Tuple[Mock, Mock]) -> Tuple[CommandQuery, Mock, Mock]:
    session, db = mock_session_with_db
    query = GetUserQuery(db_session=session)
    return query, session, db


class TestGetUserQuery:

    def test_get_user_query_initialize_correctly(self):
        session = Mock()
        query = GetUserQuery(db_session=session)

        assert isinstance(query, GetUserQuery)
        assert hasattr(query, 'db_session')
        assert query.db_session is session

    def test_get_user_query_executes_correctly(self, get_user_request,
                                               get_query_with_mocks):
        query, mock_session, db = get_query_with_mocks

        response = query.execute(request=get_user_request)

        mock_session.assert_called_once()
        db.query().filter().first.assert_called_once()

        assert bool(response) is True
        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_OK
        assert response.value.email == 'test@gmail.com'

    def test_qet_user_query_returns_exception_when_no_resource_has_been_found(self,
                                                                              get_user_request,
                                                                              get_query_with_mocks):
        query, mock_session, db = get_query_with_mocks
        db.query.return_value.filter.return_value.first.return_value = None

        response = query.execute(request=get_user_request)

        mock_session.assert_called_once()
        db.query().filter().first.assert_called_once()

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'NoMatchingUser: No User has been found for a given id: 100'

    def test_get_user_query_returns_system_error_when_generic_exception_is_raised(self,
                                                                                  get_user_request,
                                                                                  get_query_with_mocks):
        query, mock_session, db = get_query_with_mocks
        db.query.return_value.filter.return_value.first.side_effect = Exception('System error.')

        response = query.execute(request=get_user_request)

        mock_session.assert_called_once()
        db.query().filter().first.assert_called_once()

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.SYSTEM_ERROR
        assert response.message == 'Exception: System error.'
