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
def get_query_with_mock_repo(mock_user_repo: Mock) -> Tuple[CommandQuery, Mock]:
    query = GetUserQuery(repo=mock_user_repo)
    return query, mock_user_repo


class TestGetUserQuery:

    def test_get_user_query_initialize_correctly(self, get_query_with_mock_repo):
        query, repo = get_query_with_mock_repo

        assert isinstance(query, GetUserQuery)
        assert hasattr(query, 'repo')
        assert query.repo is repo

    def test_get_user_query_executes_correctly(self, get_query_with_mock_repo,
                                               get_user_request):
        query, repo = get_query_with_mock_repo

        response = query.execute(request=get_user_request)

        repo.get_user.assert_called_with(user_id='100')
        assert bool(response) is True
        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_OK
        assert response.value.email == 'test@gmail.com'

    def test_qet_user_query_returns_exception_when_no_resource_has_been_found(self,
                                                                              get_user_request):
        repo = Mock()
        repo.get_user.return_value = None
        query = GetUserQuery(repo=repo)

        response = query.execute(request=get_user_request)

        repo.get_user.assert_called_with(user_id='100')
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'NoMatchingUser: No User has been found for a given id: 100'

    def test_get_user_query_returns_system_error_when_generic_exception_is_raised(self,
                                                                                  get_user_request):
        repo = Mock()
        repo.get_user.side_effect = Exception('System error.')
        query = GetUserQuery(repo=repo)

        response = query.execute(request=get_user_request)

        repo.get_user.assert_called_with(user_id='100')
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.SYSTEM_ERROR
        assert response.message == 'Exception: System error.'
