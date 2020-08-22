import mock

from app.response_objects import ResponseSuccess, ResponseFailure
from app.application.course.commands import CreateCourseCommand


class TestCreateCourseCommand:

    def test_create_course_command_executes_correctly(self, uow):
        command = CreateCourseCommand(unit_of_work=uow)
        response = command.execute(name='Test Course')

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

    @mock.patch('app.adapters.unit_of_work.SqlAlchemyUnitOfWork')
    def test_create_course_command_returns_system_error(self, mock_uow):
        session = mock.Mock()
        session.courses.add.side_effect = Exception('System error.')
        mock_uow.__enter__.return_value = session

        command = CreateCourseCommand(unit_of_work=mock_uow)
        response = command.execute(name='Test Course')

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.SYSTEM_ERROR
        assert response.message == 'Exception: System error.'
