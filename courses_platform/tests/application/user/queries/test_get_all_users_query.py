import pytest
from mock import Mock
from typing import Tuple

from app.response_objects import ResponseSuccess
from app.application.user.queries.get_all import GetAllUsersQuery
from app.application.interfaces.icommand_query import ICommandQuery


@pytest.fixture(scope='function')
def get_all_query_with_mocks(
        mock_session_with_db: Tuple[Mock, Mock]) -> Tuple[ICommandQuery, Mock, Mock]:
    session, db = mock_session_with_db
    query = GetAllUsersQuery(db_session=session)
    return query, session, db


class TestGetAllUsersQuery:

    def test_get_all_users_query_initialize_correctly(self):
        session = Mock()
        query = GetAllUsersQuery(db_session=session)

        assert isinstance(query, GetAllUsersQuery)
        assert hasattr(query, 'db_session')
        assert query.db_session is session

    def test_get_all_users_query_returns_list_of_users(self, get_all_query_with_mocks):
        query, mock_session, db = get_all_query_with_mocks

        response = query.execute()

        mock_session.assert_called_once()
        db.query().options().all.assert_called_once_with()

        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_OK

        assert len(response.value) == 2
        assert response.value[0].id == '1'
        assert response.value[0].email == 'test@gmail.com'
        assert not hasattr(response.value, 'courses')
        assert response.value[1].id == '2'
        assert response.value[1].email == 'sample@gmail.com'
        assert not hasattr(response.value, 'courses')
