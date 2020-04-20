import pytest
from mock import Mock
from typing import Tuple

from tests.factories import UserRecord, CourseRecord

from app.domain.course import Course
from app.request_objects.user import GetUserRequest
from app.response_objects import ResponseSuccess, ResponseFailure
from app.application.interfaces.icommand_query import ICommandQuery
from app.application.user.queries.get_user_courses import GetUserCoursesQuery


@pytest.fixture
def get_user_request() -> GetUserRequest:
    return GetUserRequest(user_id='100')


@pytest.fixture(scope='function')
def get_query_with_mocks(
        mock_session_with_db: Tuple[Mock, Mock]) -> Tuple[ICommandQuery, Mock, Mock]:
    session, db = mock_session_with_db
    query = GetUserCoursesQuery(db_session=session)
    return query, session, db


class TestGetUserCoursesQuery:

    def test_get_user_courses_query_initialize_correctly(self):
        session = Mock()
        query = GetUserCoursesQuery(db_session=session)

        assert isinstance(query, GetUserCoursesQuery)
        assert hasattr(query, 'db_session')
        assert query.db_session is session

    def test_get_user_courses_executes_correctly(self, get_user_request, get_query_with_mocks):
        query, mock_session, db = get_query_with_mocks

        user = UserRecord('100', 'test@gmail.com', [CourseRecord('1', 'Test Course')])
        db.query.return_value.options.return_value.filter.return_value.first.return_value = user

        response = query.execute(request=get_user_request)

        mock_session.assert_called_once()
        db.query().options().filter().first.assert_called_once()

        assert bool(response) is True
        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_OK
        assert len(response.value) == 1
        assert isinstance(response.value[0], Course)
        assert response.value[0].name == 'Test Course'

    def test_get_user_courses_returns_resource_error(self, get_user_request, get_query_with_mocks):
        query, mock_session, db = get_query_with_mocks
        db.query.return_value.options.return_value.filter.return_value.first.return_value = None

        response = query.execute(request=get_user_request)

        mock_session.assert_called_once()
        db.query().options().filter().first.assert_called_once()

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'NoMatchingUser: No User has been found for a given id: 100'

    def test_get_user_courses_returns_system_error(self, get_user_request, get_query_with_mocks):
        query, mock_session, db = get_query_with_mocks
        db.query.return_value.options.return_value.filter.return_value.first.side_effect = Exception('System error.')

        response = query.execute(request=get_user_request)

        mock_session.assert_called_once()
        db.query().options().filter().first.assert_called_once()

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.SYSTEM_ERROR
        assert response.message == 'Exception: System error.'
