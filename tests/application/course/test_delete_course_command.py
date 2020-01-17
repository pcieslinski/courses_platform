import pytest
from mock import Mock
from typing import Tuple

from courses_platform.request_objects import Request
from courses_platform.request_objects.course import DeleteCourseRequest
from courses_platform.response_objects import ResponseSuccess, ResponseFailure
from courses_platform.application.interfaces.icommand_query import CommandQuery
from courses_platform.application.course.commands.delete import DeleteCourseCommand


@pytest.fixture
def delete_course_request() -> Request:
    return DeleteCourseRequest(course_id='100')


@pytest.fixture(scope='function')
def delete_command_with_mock_repo(mock_course_repo: Mock) -> Tuple[CommandQuery, Mock]:
    command = DeleteCourseCommand(repo=mock_course_repo)
    return command, mock_course_repo


class TestDeleteCourseCommand:

    def test_delete_course_command_initialize_correctly(self, delete_command_with_mock_repo):
        command, repo = delete_command_with_mock_repo

        assert isinstance(command, DeleteCourseCommand)
        assert hasattr(command, 'repo')
        assert command.repo is repo

    def test_delete_course_command_executes_correctly(self, delete_command_with_mock_repo,
                                                      delete_course_request):
        command, repo = delete_command_with_mock_repo

        response = command.execute(request=delete_course_request)

        repo.delete_course.assert_called_with(course_id='100')
        assert bool(response) is True
        assert isinstance(response, ResponseSuccess)
        assert response.value is 1

    def test_delete_course_command_returns_exception_when_called_with_bad_course_id(self,
                                                                                    delete_course_request):
        repo = Mock()
        repo.delete_course.side_effect = Exception(f'No match for Course with id 100.')
        command = DeleteCourseCommand(repo=repo)

        response = command.execute(request=delete_course_request)

        repo.delete_course.assert_called_with(course_id='100')
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'Exception: No match for Course with id 100.'
