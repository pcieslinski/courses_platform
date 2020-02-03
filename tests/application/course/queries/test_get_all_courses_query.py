import pytest
from mock import Mock, patch
from typing import Tuple

from app.response_objects import ResponseSuccess
from app.request_objects.course import GetAllCoursesRequest
from app.application.course.queries.get_all import GetAllCoursesQuery
from app.application.interfaces.icommand_query import CommandQuery


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

        response = query.execute(request=GetAllCoursesRequest())

        mock_session.assert_called_once()
        db.query().all.assert_called_once_with()

        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_OK

        assert len(response.value) == 2
        assert response.value[0].id == '1'
        assert response.value[0].name == 'Test Course'
        assert response.value[1].id == '2'
        assert response.value[1].name == 'Sample Course'

    @patch('app.application.course.queries.get_all.GetAllCoursesQuery._create_courses_objects_with_stats')
    def test_get_all_courses_query_returns_courses_with_stats(self, mock_creat_courses_objects_with_stats,
                                                              get_all_query_with_mocks,
                                                              courses_with_enrollments):
        mock_creat_courses_objects_with_stats.return_value = courses_with_enrollments

        query, mock_session, db = get_all_query_with_mocks

        response = query.execute(request=GetAllCoursesRequest(include=['stats']))

        mock_session.assert_called_once()
        db.query().outerjoin().group_by().all.assert_called_once()
        mock_creat_courses_objects_with_stats.assert_called_once()

        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_OK

        assert len(response.value) == 1
        assert response.value == courses_with_enrollments
