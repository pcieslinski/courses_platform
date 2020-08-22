import mock

from app.domain.course import Course
from app.application.course.queries import GetCourseQuery
from app.response_objects import ResponseSuccess, ResponseFailure


class TestGetCourseQuery:

    def test_get_course_query_executes_correctly(self, uow):
        with uow:
            uow.courses.add(Course(id='123', name='Test Course'))

        query = GetCourseQuery(unit_of_work=uow)
        response = query.execute(course_id='123')

        assert bool(response) is True
        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_OK
        assert response.value.id == '123'
        assert response.value.name == 'Test Course'

    def test_qet_course_query_returns_exception_when_no_resource_has_been_found(self, uow):
        query = GetCourseQuery(unit_of_work=uow)
        response = query.execute(course_id='123')

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'NoMatchingCourse: No Course has been found for a given id: 123'

    @mock.patch('app.adapters.unit_of_work.SqlAlchemyUnitOfWork')
    def test_get_course_query_returns_system_error_when_generic_exception_is_raised(self, mock_uow):
        session = mock.Mock()
        session.courses.get.side_effect = Exception('System error.')
        mock_uow.__enter__.return_value = session

        query = GetCourseQuery(unit_of_work=mock_uow)
        response = query.execute(course_id='123')

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.SYSTEM_ERROR
        assert response.message == 'Exception: System error.'
