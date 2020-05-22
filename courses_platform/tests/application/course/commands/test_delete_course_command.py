import mock

from app.domain.course import Course
from app.response_objects import ResponseSuccess, ResponseFailure
from app.application.course.commands.delete import DeleteCourseCommand


class TestDeleteCourseCommand:

    def test_delete_course_command_executes_correctly(self, uow):
        with uow:
            uow.courses.add(Course(id='100', name='Test Course'))

        command = DeleteCourseCommand(unit_of_work=uow)
        response = command.execute(course_id='100')

        with uow:
            course = uow.courses.get(identifier='100')

        assert bool(response) is True
        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_NO_CONTENT
        assert response.value == ''
        assert course is None

    @mock.patch('app.persistence.unit_of_work.SqlAlchemyUnitOfWork')
    def test_delete_course_command_returns_system_error_when_generic_exception_is_raised(self, mock_uow):
        session = mock.Mock()
        session.courses.remove.side_effect = Exception('System error.')
        mock_uow.__enter__.return_value = session

        command = DeleteCourseCommand(unit_of_work=mock_uow)
        response = command.execute(course_id='100')

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.SYSTEM_ERROR
        assert response.message == 'Exception: System error.'

    def test_delete_course_command_returns_resource_error_when_called_with_bad_course_id(self, uow):
        command = DeleteCourseCommand(unit_of_work=uow)
        response = command.execute(course_id='100')

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'NoMatchingCourse: No Course has been found for a given id: 100'
