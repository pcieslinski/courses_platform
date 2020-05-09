import mock
import pytest

from app.request_objects.course import CreateCourseRequest
from app.response_objects import ResponseSuccess, ResponseFailure
from app.application.course.commands.create import CreateCourseCommand


@pytest.fixture
def create_course_request() -> CreateCourseRequest:
    return CreateCourseRequest(name='Test Course')


class TestCreateCourseCommand:

    def test_create_course_command_executes_correctly(self, create_course_request, uow):
        command = CreateCourseCommand(unit_of_work=uow)
        response = command.execute(request=create_course_request)

        course_id = response.value.id
        with uow:
            course = uow.courses.get(course_id)

        assert bool(response) is True
        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_RESOURCE_CREATED
        assert response.value.name == 'Test Course'

        assert course.id == course_id
        assert course.name == 'Test Course'
        assert list(course.enrollments) == []

    @mock.patch('app.persistence.unit_of_work.SqlAlchemyUnitOfWork')
    def test_create_course_command_returns_system_error(self, mock_uow, create_course_request):
        session = mock.Mock()
        session.courses.add.side_effect = Exception('System error.')
        mock_uow.__enter__.return_value = session

        command = CreateCourseCommand(unit_of_work=mock_uow)
        response = command.execute(request=create_course_request)

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.SYSTEM_ERROR
        assert response.message == 'Exception: System error.'
