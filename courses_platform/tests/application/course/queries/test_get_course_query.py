import mock
import pytest

from app.domain.course import Course
from app.request_objects.course import GetCourseRequest
from app.application.course.queries.get import GetCourseQuery
from app.persistence.unit_of_work import SqlAlchemyUnitOfWork
from app.response_objects import ResponseSuccess, ResponseFailure


@pytest.fixture
def get_course_request() -> GetCourseRequest:
    return GetCourseRequest(course_id='123')


@pytest.fixture
def uow(session_factory) -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(session_factory)


class TestGetCourseQuery:

    def test_get_course_query_executes_correctly(self, get_course_request, uow):
        with uow:
            uow.courses.add(Course(id='123', name='Test Course'))

        query = GetCourseQuery(unit_of_work=uow)
        response = query.execute(request=get_course_request)

        assert bool(response) is True
        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_OK
        assert response.value.id == '123'
        assert response.value.name == 'Test Course'

    def test_qet_course_query_returns_exception_when_no_resource_has_been_found(
            self, get_course_request, uow
    ):
        query = GetCourseQuery(unit_of_work=uow)
        response = query.execute(request=get_course_request)

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'NoMatchingCourse: No Course has been found for a given id: 123'

    @mock.patch('app.persistence.unit_of_work.SqlAlchemyUnitOfWork')
    def test_get_course_query_returns_system_error_when_generic_exception_is_raised(
            self, mock_uow, get_course_request
    ):
        session = mock.Mock()
        session.courses.get.side_effect = Exception('System error.')
        mock_uow.__enter__.return_value = session

        query = GetCourseQuery(unit_of_work=mock_uow)
        response = query.execute(request=get_course_request)

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.SYSTEM_ERROR
        assert response.message == 'Exception: System error.'
