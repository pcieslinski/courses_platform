import pytest
from mock import Mock, patch
from typing import Tuple

from app.request_objects.course import EnrollmentRequest
from app.response_objects import ResponseSuccess, ResponseFailure
from app.application.interfaces.icommand_query import ICommandQuery
from app.application.course.commands.withdraw_user_enrollment import \
    WithdrawUserEnrollmentCommand


@pytest.fixture
def withdraw_user_enrollment_request() -> EnrollmentRequest:
    return EnrollmentRequest(course_id='10', user_id='25')


@pytest.fixture(scope='function')
def withdraw_user_enrollment_with_mocks(
        mock_session_with_db: Tuple[Mock, Mock]) -> Tuple[ICommandQuery, Mock, Mock]:
    session, db = mock_session_with_db
    command = WithdrawUserEnrollmentCommand(db_session=session)
    return command, session, db


class TestWithdrawUserEnrollmentCommand:

    def test_withdraw_user_enrollment_initialize_correctly(self):
        session = Mock()
        command = WithdrawUserEnrollmentCommand(db_session=session)

        assert isinstance(command, WithdrawUserEnrollmentCommand)
        assert hasattr(command, 'db_session')
        assert command.db_session is session

    @patch('app.application.course.commands.withdraw_user_enrollment.WithdrawUserEnrollmentCommand.user_is_enrolled')
    def test_withdraw_user_enrollment_executes_correctly(self, mock_user_is_enrolled,
                                                         withdraw_user_enrollment_request,
                                                         withdraw_user_enrollment_with_mocks):
        mock_user_is_enrolled.return_value = True
        command, mock_session, db = withdraw_user_enrollment_with_mocks
        db.query.return_value.filter_by.return_value.first.return_value = Mock()

        response = command.execute(request=withdraw_user_enrollment_request)

        mock_session.assert_called_once()
        db.query().filter_by().first.assert_called_once()
        db.query().options().filter_by().first.assert_called_once()

        assert bool(response) is True
        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_NO_CONTENT
        assert response.value == ''

    def test_withdraw_user_enrollment_returns_no_matching_course_error(self,
                                                                       withdraw_user_enrollment_request,
                                                                       withdraw_user_enrollment_with_mocks):
        command, mock_session, db = withdraw_user_enrollment_with_mocks
        db.query.return_value.filter_by.return_value.first.return_value = None

        response = command.execute(request=withdraw_user_enrollment_request)

        mock_session.assert_called_once()
        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'NoMatchingCourse: No Course has been found for a given id: 10'

    def test_withdraw_user_enrollment_returns_no_matching_user_error(self,
                                                                     withdraw_user_enrollment_request,
                                                                     withdraw_user_enrollment_with_mocks):
        command, mock_session, db = withdraw_user_enrollment_with_mocks
        db.query.return_value.filter_by.return_value.first.side_effect = 'course'
        db.query.return_value.options.return_value.filter_by.return_value.first.return_value = None

        response = command.execute(request=withdraw_user_enrollment_request)

        mock_session.assert_called_once()
        db.query().filter_by().first.assert_called_once()
        db.query().options().filter_by().first.assert_called_once()

        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'NoMatchingUser: No User has been found for a given id: 25'

    @patch('app.application.course.commands.withdraw_user_enrollment.WithdrawUserEnrollmentCommand.user_is_enrolled')
    def test_withdraw_user_enrollment_returns_user_not_enrolled_error(self,
                                                                      mock_user_is_enrolled,
                                                                      withdraw_user_enrollment_request,
                                                                      withdraw_user_enrollment_with_mocks):
        mock_user_is_enrolled.return_value = False
        command, mock_session, db = withdraw_user_enrollment_with_mocks

        response = command.execute(request=withdraw_user_enrollment_request)

        mock_session.assert_called_once()
        db.query().filter_by().first.assert_called_once()
        db.query().options().filter_by().first.assert_called_once()

        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'UserNotEnrolled: User: 25 is not enrolled in Course: 10'

    def test_withdraw_user_enrollment_returns_system_error(self,
                                                           withdraw_user_enrollment_request,
                                                           withdraw_user_enrollment_with_mocks):
        command, mock_session, db = withdraw_user_enrollment_with_mocks
        db.query.return_value.filter_by.return_value.first.side_effect = Exception('Some error')

        response = command.execute(request=withdraw_user_enrollment_request)

        mock_session.assert_called_once()
        assert bool(response) is False
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.SYSTEM_ERROR
        assert response.message == 'Exception: Some error'
