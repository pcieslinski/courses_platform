import pytest
from mock import Mock
from uuid import uuid4
from typing import Tuple

from courses_platform.application.interfaces.icommand_query import CommandQuery
from courses_platform.application.course.commands.delete import DeleteCourseCommand, NoMatchingCourse


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

    def test_delete_course_command_executes_correctly(self, course, delete_command_with_mock_repo):
        course_id = course.id
        command, repo = delete_command_with_mock_repo

        result = command.execute(course_id=course_id)

        repo.delete_course.assert_called_with(course_id=course_id)
        assert result

    def test_delete_course_command_returns_exception_when_called_with_bad_course_id(self):
        course_id = str(uuid4())

        repo = Mock()
        repo.delete_course.side_effect = NoMatchingCourse(f'No match for Course with id {course_id}.')
        command = DeleteCourseCommand(repo=repo)

        with pytest.raises(NoMatchingCourse) as exc:
            result = command.execute(course_id=course_id)

            repo.delete_course.assert_called_with(course_id=course_id)
            assert str(exc) == f'No match for Course with id {course_id}.'
