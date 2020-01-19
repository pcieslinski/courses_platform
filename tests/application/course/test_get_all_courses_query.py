import pytest
from mock import Mock
from typing import Tuple

from courses_platform.response_objects import ResponseSuccess
from courses_platform.application.course.queries.get_all import GetAllCoursesQuery
from courses_platform.application.interfaces.icommand_query import CommandQuery


@pytest.fixture(scope='function')
def get_all_query_with_mocks(
        mock_session_with_db: Tuple[Mock, Mock]) -> Tuple[CommandQuery, Mock, Mock]:
    session, db = mock_session_with_db
    query = GetAllCoursesQuery(db_session=session)
    return query, session, db


class TestGetAllCoursesQuery:

    def test_get_all_courses_query_initialize_correctly(self):
        session = Mock()
        query = GetAllCoursesQuery(db_session=session)

        assert isinstance(query, GetAllCoursesQuery)
        assert hasattr(query, 'db_session')
        assert query.db_session is session

    def test_get_all_courses_query_executes_correctly(self, get_all_query_with_mocks):
        query, mock_session, db = get_all_query_with_mocks

        response = query.execute()

        mock_session.assert_called_once()
        db.query().all.assert_called_once_with()

        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_OK

        assert len(response.value) == 2
        assert response.value[0].id == '1'
        assert response.value[0].name == 'Test Course'
        assert response.value[1].id == '2'
        assert response.value[1].name == 'Sample Course'
