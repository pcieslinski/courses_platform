import pytest
from mock import Mock
from typing import Tuple

from app.request_objects.course import CreateCourseRequest
from app.response_objects import ResponseSuccess, ResponseFailure
from app.application.interfaces.icommand_query import ICommandQuery
from app.application.course.commands.create import CreateCourseCommand


@pytest.fixture
def create_course_request() -> CreateCourseRequest:
    return CreateCourseRequest(name='Test Course')


@pytest.fixture(scope='function')
def create_command_with_mocks(
        mock_session_with_db: Tuple[Mock, Mock]) -> Tuple[ICommandQuery, Mock, Mock]:
    session, db = mock_session_with_db
    command = CreateCourseCommand(db_session=session)
    return command, session, db


class TestCreateCourseCommand:

    def test_create_course_command_initialize_correctly(self):
        session = Mock()
        command = CreateCourseCommand(db_session=session)

        assert isinstance(command, CreateCourseCommand)
        assert hasattr(command, 'db_session')
        assert command.db_session is session

    def test_create_course_command_executes_correctly(self, create_course_request,
                                                      create_command_with_mocks):
        command, mock_session, db = create_command_with_mocks

        response = command.execute(request=create_course_request)

        mock_session.assert_called_once()
        db.add.assert_called_once()

        assert bool(response) is True
        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_RESOURCE_CREATED
        assert response.value.name == 'Test Course'

    def test_create_course_command_returns_exception(self, create_course_request,
                                                     create_command_with_mocks):
        command, mock_session, db = create_command_with_mocks
        db.add.side_effect = Exception(
            'Course with "Test Course" name already exists.'
        )

        response = command.execute(request=create_course_request)

        mock_session.assert_called_once()
        db.add.assert_called_once()

        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'Exception: Course with "Test Course" name already exists.'
