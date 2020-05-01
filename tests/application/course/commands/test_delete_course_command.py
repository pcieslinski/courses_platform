import pytest
from mock import Mock
from typing import Tuple

from app.request_objects.course import DeleteCourseRequest
from app.response_objects import ResponseSuccess, ResponseFailure
from app.application.interfaces.icommand_query import ICommandQuery
from app.application.course.commands.delete import DeleteCourseCommand


@pytest.fixture
def delete_course_request() -> DeleteCourseRequest:
    return DeleteCourseRequest(course_id='100')


@pytest.fixture(scope='function')
def delete_command_with_mocks(
        mock_session_with_db: Tuple[Mock, Mock]) -> Tuple[ICommandQuery, Mock, Mock]:
    session, db = mock_session_with_db
    command = DeleteCourseCommand(db_session=session)
    return command, session, db


class TestDeleteCourseCommand:

    def test_delete_course_command_initialize_correctly(self):
        session = Mock()
        command = DeleteCourseCommand(db_session=session)

        assert isinstance(command, DeleteCourseCommand)
        assert hasattr(command, 'db_session')
        assert command.db_session is session

    def test_delete_course_command_executes_correctly(self, delete_course_request,
                                                      delete_command_with_mocks):
        command, mock_session, db = delete_command_with_mocks

        response = command.execute(request=delete_course_request)

        mock_session.assert_called_once()
        db.delete.assert_called_once()

        assert bool(response) is True
        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_NO_CONTENT
        assert response.value == ''

    def test_delete_course_command_returns_system_error_when_generic_exception_is_raised(self,
                                                                                         delete_course_request,
                                                                                         delete_command_with_mocks):
        command, mock_session, db = delete_command_with_mocks
        db.delete.side_effect = Exception('System error.')

        response = command.execute(request=delete_course_request)

        mock_session.assert_called_once()
        db.delete.assert_called_once()

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.SYSTEM_ERROR
        assert response.message == 'Exception: System error.'

    def test_delete_course_command_returns_resource_error_when_called_with_bad_course_id(self,
                                                                                         delete_course_request,
                                                                                         delete_command_with_mocks):
        command, mock_session, db = delete_command_with_mocks
        db.query.return_value.filter_by.return_value.first.return_value = None

        response = command.execute(request=delete_course_request)

        mock_session.assert_called_once()
        assert db.delete.call_count == 0

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'NoMatchingCourse: No Course has been found for a given id: 100'
