import mock

from app.domain.user import User
from app.domain.course import Course
from app.response_objects import ResponseSuccess, ResponseFailure
from app.application.course.commands.withdraw_user_enrollment import WithdrawUserEnrollmentCommand


class TestWithdrawUserEnrollmentCommand:

    def test_withdraw_user_enrollment_executes_correctly(self, session_factory, uow):
        with uow:
            user = User(id='25', email='test@gmail.com')
            course = Course(id='10', name='Test Course')

            course.enrollments.append(user)

            uow.users.add(user)
            uow.courses.add(course)

        command = WithdrawUserEnrollmentCommand(unit_of_work=uow)
        response = command.execute(course_id='10', user_id='25')

        session = session_factory()
        enrollments = list(session.execute(
            'SELECT course_id, user_id FROM "enrollment"'
        ))

        assert bool(response) is True
        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_NO_CONTENT
        assert response.value == ''
        assert enrollments == []

    def test_withdraw_user_enrollment_returns_no_matching_course_error(self, uow):
        command = WithdrawUserEnrollmentCommand(unit_of_work=uow)
        response = command.execute(course_id='10', user_id='25')

        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'NoMatchingCourse: No Course has been found for a given id: 10'

    def test_withdraw_user_enrollment_returns_no_matching_user_error(self, uow):
        with uow:
            uow.courses.add(Course(id='10', name='Test Course'))

        command = WithdrawUserEnrollmentCommand(unit_of_work=uow)
        response = command.execute(course_id='10', user_id='25')

        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'NoMatchingUser: No User has been found for a given id: 25'

    def test_withdraw_user_enrollment_returns_user_not_enrolled_error(self, uow):
        with uow:
            uow.users.add(User(id='25', email='test@gmail.com'))
            uow.courses.add(Course(id='10', name='Test Course'))

        command = WithdrawUserEnrollmentCommand(unit_of_work=uow)
        response = command.execute(course_id='10', user_id='25')

        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'UserNotEnrolled: User: 25 is not enrolled in Course: 10'

    @mock.patch('app.persistence.unit_of_work.SqlAlchemyUnitOfWork')
    def test_withdraw_user_enrollment_returns_system_error(self, mock_uow):
        session = mock.Mock()
        session.courses.get.side_effect = Exception('System error.')
        mock_uow.__enter__.return_value = session

        command = WithdrawUserEnrollmentCommand(unit_of_work=mock_uow)
        response = command.execute(course_id='10', user_id='25')

        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.SYSTEM_ERROR
        assert response.message == 'Exception: System error.'
