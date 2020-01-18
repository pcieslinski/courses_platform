import pytest
from mock import Mock
from typing import Tuple

from courses_platform.response_objects import ResponseSuccess
from courses_platform.application.user.queries.get_all import GetAllUsersQuery
from courses_platform.application.interfaces.icommand_query import CommandQuery


@pytest.fixture(scope='function')
def get_all_query_with_mock_repo(mock_user_repo: Mock) -> Tuple[CommandQuery, Mock]:
    query = GetAllUsersQuery(mock_user_repo)
    return query, mock_user_repo


class TestGetAllUsersQuery:

    def test_get_all_users_query_initialize_correctly(self, get_all_query_with_mock_repo):
        query, repo = get_all_query_with_mock_repo

        assert isinstance(query, GetAllUsersQuery)
        assert hasattr(query, 'repo')
        assert query.repo is repo

    def test_get_all_users_query_returns_list_of_users(self, users, get_all_query_with_mock_repo):
        query, repo = get_all_query_with_mock_repo

        response = query.execute()

        repo.get_all_users.assert_called_with()
        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_OK
        assert response.value == users
