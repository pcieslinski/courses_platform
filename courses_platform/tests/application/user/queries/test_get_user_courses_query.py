import mock
import pytest

from app.domain.user import User
from app.domain.course import Course
from app.request_objects.user import GetUserRequest
from app.persistence.unit_of_work import SqlAlchemyUnitOfWork
from app.response_objects import ResponseSuccess, ResponseFailure
from app.application.user.queries.get_user_courses import GetUserCoursesQuery


@pytest.fixture
def get_user_request() -> GetUserRequest:
    return GetUserRequest(user_id='1')


@pytest.fixture
def uow(session_factory) -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(session_factory)


class TestGetUserCoursesQuery:

    def test_get_user_courses_executes_correctly(self, get_user_request, uow):
        with uow:
            user = User(id='1',
                        email='test@gmail.com',
                        courses=[Course(id='100', name='Test Course')])

            uow.users.add(user)

        query = GetUserCoursesQuery(unit_of_work=uow)
        response = query.execute(request=get_user_request)

        assert bool(response) is True
        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_OK
        assert len(response.value) == 1
        assert isinstance(response.value[0], Course)
        assert response.value[0].id == '100'
        assert response.value[0].name == 'Test Course'

    def test_get_user_courses_returns_resource_error(self, get_user_request, uow):
        query = GetUserCoursesQuery(unit_of_work=uow)
        response = query.execute(request=get_user_request)

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'NoMatchingUser: No User has been found for a given id: 1'

    @mock.patch('app.persistence.unit_of_work.SqlAlchemyUnitOfWork')
    def test_get_user_courses_returns_system_error(self, mock_uow, get_user_request):
        session = mock.Mock()
        session.users.get.side_effect = Exception('System error.')
        mock_uow.__enter__.return_value = session

        query = GetUserCoursesQuery(unit_of_work=mock_uow)
        response = query.execute(request=get_user_request)

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.SYSTEM_ERROR
        assert response.message == 'Exception: System error.'
