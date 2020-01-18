import pytest
from mock import Mock
from typing import Tuple

from courses_platform.request_objects import Request
from courses_platform.request_objects.course import CreateCourseRequest
from courses_platform.response_objects import ResponseSuccess, ResponseFailure
from courses_platform.application.interfaces.icommand_query import CommandQuery
from courses_platform.application.course.commands.create import CreateCourseCommand


@pytest.fixture
def create_course_request() -> Request:
    return CreateCourseRequest(name='Test Course')


@pytest.fixture(scope='function')
def create_command_with_mock_repo(mock_course_repo: Mock) -> Tuple[CommandQuery, Mock]:
    command = CreateCourseCommand(repo=mock_course_repo)
    return command, mock_course_repo


class TestCreateCourseCommand:

    def test_create_course_command_initialize_correctly(self, create_command_with_mock_repo):
        command, repo = create_command_with_mock_repo

        assert isinstance(command, CreateCourseCommand)
        assert hasattr(command, 'repo')
        assert command.repo is repo

    def test_create_course_command_executes_correctly(self, create_command_with_mock_repo,
                                                      create_course_request):
        command, repo = create_command_with_mock_repo

        response = command.execute(request=create_course_request)

        repo.create_course.assert_called_with(name='Test Course')
        assert bool(response) is True
        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_RESOURCE_CREATED
        assert response.value.name == 'Test Course'

    def test_create_course_command_returns_exception(self, create_course_request):
        repo = Mock()
        repo.create_course.side_effect = Exception(
            'Course with "Test Course" name already exists.'
        )
        command = CreateCourseCommand(repo=repo)

        response = command.execute(request=create_course_request)

        repo.create_course.assert_called_with(name='Test Course')
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'Exception: Course with "Test Course" name already exists.'
