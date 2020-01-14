import pytest
from mock import Mock
from typing import Tuple

from courses_platform.application.course.queries.get_all import GetAllCoursesQuery
from courses_platform.application.interfaces.icommand_query import CommandQuery


@pytest.fixture(scope='function')
def get_all_query_with_mock_repo(mock_course_repo: Mock) -> Tuple[CommandQuery, Mock]:
    query = GetAllCoursesQuery(repo=mock_course_repo)
    return query, mock_course_repo


class TestGetAllCoursesQuery:

    def test_get_all_courses_query_initialize_correctly(self, get_all_query_with_mock_repo):
        query, repo = get_all_query_with_mock_repo

        assert isinstance(query, GetAllCoursesQuery)
        assert hasattr(query, 'repo')
        assert query.repo is repo

    def test_get_all_courses_query_executes_correctly(self, courses, get_all_query_with_mock_repo):
        query, repo = get_all_query_with_mock_repo

        result = query.execute()

        repo.get_all_courses.assert_called_with()
        assert result == courses
