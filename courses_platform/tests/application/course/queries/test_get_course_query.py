import pytest
from mock import Mock
from typing import Tuple

from app.request_objects.course import GetCourseRequest
from app.response_objects import ResponseSuccess, ResponseFailure
from app.application.course.queries.get import GetCourseQuery
from app.application.interfaces.icommand_query import ICommandQuery


@pytest.fixture
def get_course_request() -> GetCourseRequest:
    return GetCourseRequest(course_id='123')


@pytest.fixture(scope='function')
def get_query_with_mocks(
        mock_session_with_db: Tuple[Mock, Mock]) -> Tuple[ICommandQuery, Mock, Mock]:
    session, db = mock_session_with_db
    query = GetCourseQuery(db_session=session)
    return query, session, db


class TestGetCourseQuery:

    def test_get_course_query_initialize_correctly(self):
        session = Mock()
        query = GetCourseQuery(db_session=session)

        assert isinstance(query, GetCourseQuery)
        assert hasattr(query, 'db_session')
        assert query.db_session is session

    def test_get_course_query_executes_correctly(self, get_course_request,
                                                 get_query_with_mocks):
        query, mock_session, db = get_query_with_mocks

        response = query.execute(request=get_course_request)

        mock_session.assert_called_once()
        db.query().filter().first.assert_called_once()

        assert bool(response) is True
        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_OK
        assert response.value.name == 'Test Course'

    def test_qet_course_query_returns_exception_when_no_resource_has_been_found(self,
                                                                                get_course_request,
                                                                                get_query_with_mocks):
        query, mock_session, db = get_query_with_mocks
        db.query.return_value.filter.return_value.first.return_value = None

        response = query.execute(request=get_course_request)

        mock_session.assert_called_once()
        db.query().filter().first.assert_called_once()

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'NoMatchingCourse: No Course has been found for a given id: 123'

    def test_get_course_query_returns_system_error_when_generic_exception_is_raised(self,
                                                                                    get_course_request,
                                                                                    get_query_with_mocks):
        query, mock_session, db = get_query_with_mocks
        db.query.return_value.filter.return_value.first.side_effect = Exception('System error.')

        response = query.execute(request=get_course_request)

        mock_session.assert_called_once()
        db.query().filter().first.assert_called_once()

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.SYSTEM_ERROR
        assert response.message == 'Exception: System error.'
