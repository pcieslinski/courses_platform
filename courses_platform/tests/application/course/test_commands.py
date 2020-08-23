import mock

from app.domain.user import User
from app.domain.course import Course
from app.application.course import commands
from app.response_objects import ResponseSuccess, ResponseFailure


class TestCreateCourseCommand:

    def test_create_course_command_executes_correctly(self, uow):
        command = commands.CreateCourseCommand(unit_of_work=uow)
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

        command = commands.CreateCourseCommand(unit_of_work=mock_uow)
        response = command.execute(name='Test Course')

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.SYSTEM_ERROR
        assert response.message == 'Exception: System error.'


class TestDeleteCourseCommand:

    def test_delete_course_command_executes_correctly(self, uow):
        with uow:
            uow.courses.add(Course(id='100', name='Test Course'))

        command = commands.DeleteCourseCommand(unit_of_work=uow)
        response = command.execute(course_id='100')

        with uow:
            course = uow.courses.get(identifier='100')

        assert bool(response) is True
        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_NO_CONTENT
        assert response.value == ''
        assert course is None

    @mock.patch('app.adapters.unit_of_work.SqlAlchemyUnitOfWork')
    def test_delete_course_command_returns_system_error_when_generic_exception_is_raised(self, mock_uow):
        session = mock.Mock()
        session.courses.remove.side_effect = Exception('System error.')
        mock_uow.__enter__.return_value = session

        command = commands.DeleteCourseCommand(unit_of_work=mock_uow)
        response = command.execute(course_id='100')

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.SYSTEM_ERROR
        assert response.message == 'Exception: System error.'

    def test_delete_course_command_returns_resource_error_when_called_with_bad_course_id(self, uow):
        command = commands.DeleteCourseCommand(unit_of_work=uow)
        response = command.execute(course_id='100')

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'NoMatchingCourse: No Course has been found for a given id: 100'


class TestEnrollUserCommand:

    def test_enroll_user_command_executes_correctly(self, session_factory, uow):
        with uow:
            uow.users.add(User(id='20', email='test@gmail.com'))
            uow.courses.add(Course(id='100', name='Test Course'))

        command = commands.EnrollUserCommand(unit_of_work=uow)
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
        command = commands.EnrollUserCommand(unit_of_work=uow)
        response = command.execute(course_id='100', user_id='20')

        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'NoMatchingCourse: No Course has been found for a given id: 100'

    def test_enroll_user_command_returns_no_matching_user_error(self, uow):
        with uow:
            uow.courses.add(Course(id='100', name='Test Course'))

        command = commands.EnrollUserCommand(unit_of_work=uow)
        response = command.execute(course_id='100', user_id='20')

        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'NoMatchingUser: No User has been found for a given id: 20'

    def test_enroll_user_command_returns_user_already_enrolled_error(self, uow):
        with uow:
            user = User(id='20', email='test@gmail.com')
            course = Course(id='100', name='Test Course')

            course.enroll(user)

            uow.users.add(user)
            uow.courses.add(course)

        command = commands.EnrollUserCommand(unit_of_work=uow)
        response = command.execute(course_id='100', user_id='20')

        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'UserAlreadyEnrolled: User: 20 is already enrolled in Course: 100'

    @mock.patch('app.adapters.unit_of_work.SqlAlchemyUnitOfWork')
    def test_enroll_user_command_returns_system_error(self, mock_uow):
        session = mock.Mock()
        session.courses.get.side_effect = Exception('System error.')
        mock_uow.__enter__.return_value = session

        command = commands.EnrollUserCommand(unit_of_work=mock_uow)
        response = command.execute(course_id='100', user_id='20')

        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.SYSTEM_ERROR
        assert response.message == 'Exception: System error.'


class TestWithdrawUserEnrollmentCommand:

    def test_withdraw_user_enrollment_executes_correctly(self, session_factory, uow):
        with uow:
            user = User(id='25', email='test@gmail.com')
            course = Course(id='10', name='Test Course')

            course.enroll(user)

            uow.users.add(user)
            uow.courses.add(course)

        command = commands.WithdrawUserEnrollmentCommand(unit_of_work=uow)
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
        command = commands.WithdrawUserEnrollmentCommand(unit_of_work=uow)
        response = command.execute(course_id='10', user_id='25')

        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'NoMatchingCourse: No Course has been found for a given id: 10'

    def test_withdraw_user_enrollment_returns_no_matching_user_error(self, uow):
        with uow:
            uow.courses.add(Course(id='10', name='Test Course'))

        command = commands.WithdrawUserEnrollmentCommand(unit_of_work=uow)
        response = command.execute(course_id='10', user_id='25')

        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'NoMatchingUser: No User has been found for a given id: 25'

    def test_withdraw_user_enrollment_returns_user_not_enrolled_error(self, uow):
        with uow:
            uow.users.add(User(id='25', email='test@gmail.com'))
            uow.courses.add(Course(id='10', name='Test Course'))

        command = commands.WithdrawUserEnrollmentCommand(unit_of_work=uow)
        response = command.execute(course_id='10', user_id='25')

        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'UserNotEnrolled: User: 25 is not enrolled in Course: 10'

    @mock.patch('app.adapters.unit_of_work.SqlAlchemyUnitOfWork')
    def test_withdraw_user_enrollment_returns_system_error(self, mock_uow):
        session = mock.Mock()
        session.courses.get.side_effect = Exception('System error.')
        mock_uow.__enter__.return_value = session

        command = commands.WithdrawUserEnrollmentCommand(unit_of_work=mock_uow)
        response = command.execute(course_id='10', user_id='25')

        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.SYSTEM_ERROR
        assert response.message == 'Exception: System error.'
