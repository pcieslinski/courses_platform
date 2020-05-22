import mock

from app.domain.user import User
from app.domain.course import Course
from app.response_objects import ResponseSuccess, ResponseFailure
from app.application.course.commands.enroll_user import EnrollUserCommand


class TestEnrollUserCommand:

    def test_enroll_user_command_executes_correctly(self, session_factory, uow):
        with uow:
            uow.users.add(User(id='20', email='test@gmail.com'))
            uow.courses.add(Course(id='100', name='Test Course'))

        command = EnrollUserCommand(unit_of_work=uow)
        response = command.execute(course_id='100', user_id='20')

        session = session_factory()
        enrollments = list(session.execute(
            'SELECT course_id, user_id FROM "enrollment"'
        ))

        assert bool(response) is True
        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_RESOURCE_CREATED
        assert response.value['course_id'] == '100'
        assert response.value['user_id'] == '20'

        assert enrollments[0][0] == '100'
        assert enrollments[0][1] == '20'

    def test_enroll_user_command_returns_no_matching_course_error(self, uow):
        command = EnrollUserCommand(unit_of_work=uow)
        response = command.execute(course_id='100', user_id='20')

        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'NoMatchingCourse: No Course has been found for a given id: 100'

    def test_enroll_user_command_returns_no_matching_user_error(self, uow):
        with uow:
            uow.courses.add(Course(id='100', name='Test Course'))

        command = EnrollUserCommand(unit_of_work=uow)
        response = command.execute(course_id='100', user_id='20')

        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'NoMatchingUser: No User has been found for a given id: 20'

    def test_enroll_user_command_returns_user_already_enrolled_error(self, uow):
        with uow:
            user = User(id='20', email='test@gmail.com')
            course = Course(id='100', name='Test Course')

            course.enrollments.append(user)

            uow.users.add(user)
            uow.courses.add(course)

        command = EnrollUserCommand(unit_of_work=uow)
        response = command.execute(course_id='100', user_id='20')

        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'UserAlreadyEnrolled: User: 20 is already enrolled in Course: 100'

    @mock.patch('app.persistence.unit_of_work.SqlAlchemyUnitOfWork')
    def test_enroll_user_command_returns_system_error(self, mock_uow):
        session = mock.Mock()
        session.courses.get.side_effect = Exception('System error.')
        mock_uow.__enter__.return_value = session

        command = EnrollUserCommand(unit_of_work=mock_uow)
        response = command.execute(course_id='100', user_id='20')

        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.SYSTEM_ERROR
        assert response.message == 'Exception: System error.'
