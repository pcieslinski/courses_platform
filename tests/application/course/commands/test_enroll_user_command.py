import pytest
from mock import Mock, patch
from typing import Tuple

from courses_platform.request_objects import Request
from courses_platform.request_objects.course import EnrollmentRequest
from courses_platform.response_objects import ResponseSuccess, ResponseFailure
from courses_platform.application.interfaces.icommand_query import CommandQuery
from courses_platform.application.course.commands.enroll_user import EnrollUserCommand


@pytest.fixture
def enroll_user_request() -> Request:
    return EnrollmentRequest(course_id='100', user_id='20')


@pytest.fixture(scope='function')
def enroll_user_command_with_mocks(
        mock_session_with_db: Tuple[Mock, Mock]) -> Tuple[CommandQuery, Mock, Mock]:
    session, db = mock_session_with_db
    command = EnrollUserCommand(db_session=session)
    return command, session, db


class TestEnrollUserCommand:

    def test_enroll_user_command_initialize_correctly(self):
        session = Mock()
        command = EnrollUserCommand(db_session=session)

        assert isinstance(command, EnrollUserCommand)
        assert hasattr(command, 'db_session')
        assert command.db_session is session

    @patch('courses_platform.application.course.commands.enroll_user.EnrollUserCommand.user_is_enrolled')
    def test_enroll_user_command_executes_correctly(self, mock_user_is_enrolled, enroll_user_request,
                                                    enroll_user_command_with_mocks):
        mock_user_is_enrolled.return_value = False
        command, mock_session, db = enroll_user_command_with_mocks
        db.query.return_value.filter.return_value.first.return_value = Mock()

        response = command.execute(request=enroll_user_request)

        mock_session.assert_called_once()
        assert db.query().filter().first.call_count == 2

        assert bool(response) is True
        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_RESOURCE_CREATED
        assert response.value['course_id'] == '100'
        assert response.value['user_id'] == '20'

    def test_enroll_user_command_returns_no_matching_course_error(self, enroll_user_request,
                                                                  enroll_user_command_with_mocks):
        command, mock_session, db = enroll_user_command_with_mocks
        db.query.return_value.filter.return_value.first.return_value = None

        response = command.execute(request=enroll_user_request)

        mock_session.assert_called_once()
        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'NoMatchingCourse: No Course has been found for a given id: 100'
    
    def test_enroll_user_command_returns_no_matching_user_error(self, enroll_user_request,
                                                                enroll_user_command_with_mocks):
        command, mock_session, db = enroll_user_command_with_mocks
        db.query.return_value.filter.return_value.first.side_effect = ['course', None]

        response = command.execute(request=enroll_user_request)

        mock_session.assert_called_once()
        assert db.query().filter().first.call_count == 2

        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'NoMatchingUser: No User has been found for a given id: 20'

    @patch('courses_platform.application.course.commands.enroll_user.EnrollUserCommand.user_is_enrolled')
    def test_enroll_user_command_returns_user_already_enrolled_error(self, mock_user_is_enrolled,
                                                                     enroll_user_request,
                                                                     enroll_user_command_with_mocks):
        mock_user_is_enrolled.return_value = True
        command, mock_session, db = enroll_user_command_with_mocks

        response = command.execute(request=enroll_user_request)

        mock_session.assert_called_once()
        assert db.query().filter().first.call_count == 2

        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'UserAlreadyEnrolled: User: 20 is already enrolled in Course: 100'

    def test_enroll_user_command_returns_system_error(self, enroll_user_request,
                                                      enroll_user_command_with_mocks):
        command, mock_session, db = enroll_user_command_with_mocks
        db.query.return_value.filter.return_value.first.side_effect = Exception('Generic error')

        response = command.execute(request=enroll_user_request)

        mock_session.assert_called_once()
        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.SYSTEM_ERROR
        assert response.message == 'Exception: Generic error'
