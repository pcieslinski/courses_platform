import mock
import pytest

from app.domain.user import User
from app.domain.course import Course
from app.request_objects.course import EnrollmentRequest
from app.persistence.unit_of_work import SqlAlchemyUnitOfWork
from app.response_objects import ResponseSuccess, ResponseFailure
from app.application.course.commands.enroll_user import EnrollUserCommand


@pytest.fixture
def enroll_user_request() -> EnrollmentRequest:
    return EnrollmentRequest(course_id='100', user_id='20')


@pytest.fixture
def uow(session_factory) -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(session_factory)


class TestEnrollUserCommand:

    def test_enroll_user_command_executes_correctly(self, enroll_user_request, session_factory, uow):
        with uow:
            uow.users.add(User(id='20', email='test@gmail.com'))
            uow.courses.add(Course(id='100', name='Test Course'))

        command = EnrollUserCommand(unit_of_work=uow)
        response = command.execute(request=enroll_user_request)

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

    def test_enroll_user_command_returns_no_matching_course_error(self, enroll_user_request, uow):
        command = EnrollUserCommand(unit_of_work=uow)
        response = command.execute(request=enroll_user_request)

        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'NoMatchingCourse: No Course has been found for a given id: 100'

    def test_enroll_user_command_returns_no_matching_user_error(self, enroll_user_request, uow):
        with uow:
            uow.courses.add(Course(id='100', name='Test Course'))

        command = EnrollUserCommand(unit_of_work=uow)
        response = command.execute(request=enroll_user_request)

        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'NoMatchingUser: No User has been found for a given id: 20'

    def test_enroll_user_command_returns_user_already_enrolled_error(self, enroll_user_request, uow):
        with uow:
            user = User(id='20', email='test@gmail.com')
            course = Course(id='100', name='Test Course')

            course.enrollments.append(user)

            uow.users.add(user)
            uow.courses.add(course)

        command = EnrollUserCommand(unit_of_work=uow)
        response = command.execute(request=enroll_user_request)

        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'UserAlreadyEnrolled: User: 20 is already enrolled in Course: 100'

    @mock.patch('app.persistence.unit_of_work.SqlAlchemyUnitOfWork')
    def test_enroll_user_command_returns_system_error(self, mock_uow, enroll_user_request):
        session = mock.Mock()
        session.courses.get.side_effect = Exception('System error.')
        mock_uow.__enter__.return_value = session

        command = EnrollUserCommand(unit_of_work=mock_uow)
        response = command.execute(request=enroll_user_request)

        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.SYSTEM_ERROR
        assert response.message == 'Exception: System error.'
