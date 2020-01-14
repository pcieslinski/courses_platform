import pytest
from mock import Mock
from typing import Tuple

from courses_platform.application.interfaces.icommand_query import CommandQuery
from courses_platform.application.course.commands.create import CreateCourseCommand, CourseAlreadyExists


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

    def test_create_course_command_executes_correctly(self, create_command_with_mock_repo):
        command, repo = create_command_with_mock_repo

        result = command.execute(name='Test Course')

        repo.create_course.assert_called_with(name='Test Course')
        assert result.name == 'Test Course'

    def test_create_course_command_returns_exception_when_called_with_already_existing_course_name(self):
        repo = Mock()
        repo.create_course.side_effect = CourseAlreadyExists(
            'Course with "Test Course" name already exists.'
        )
        command = CreateCourseCommand(repo=repo)

        result = command.execute(name='Test Course')

        repo.create_course.assert_called_with(name='Test Course')
        assert isinstance(result, CourseAlreadyExists)
        assert str(result) == 'Course with "Test Course" name already exists.'
