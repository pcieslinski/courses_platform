import pytest
from mock import Mock
from typing import Tuple

from courses_platform.request_objects import Request
from courses_platform.request_objects.course import GetCourseRequest
from courses_platform.response_objects import ResponseSuccess, ResponseFailure
from courses_platform.application.course.queries.get import GetCourseQuery
from courses_platform.application.interfaces.icommand_query import CommandQuery


@pytest.fixture
def get_course_request() -> Request:
    return GetCourseRequest(course_id='123')


@pytest.fixture(scope='function')
def get_query_with_mock_repo(mock_course_repo: Mock) -> Tuple[CommandQuery, Mock]:
    query = GetCourseQuery(repo=mock_course_repo)
    return query, mock_course_repo


class TestGetCourseQuery:

    def test_get_course_query_initialize_correctly(self, get_query_with_mock_repo):
        query, repo = get_query_with_mock_repo

        assert isinstance(query, GetCourseQuery)
        assert hasattr(query, 'repo')
        assert query.repo is repo

    def test_get_course_query_executes_correctly(self, get_query_with_mock_repo,
                                                 get_course_request):
        query, repo = get_query_with_mock_repo

        response = query.execute(request=get_course_request)

        repo.get_course.assert_called_with(course_id='123')
        assert bool(response) is True
        assert isinstance(response, ResponseSuccess)
        assert response.type == ResponseSuccess.SUCCESS_OK
        assert response.value.name == 'Test Course'

    def test_qet_course_query_returns_exception_when_no_resource_has_been_found(self,
                                                                                get_course_request):
        repo = Mock()
        repo.get_course.return_value = None
        query = GetCourseQuery(repo=repo)

        response = query.execute(request=get_course_request)

        repo.get_course.assert_called_with(course_id='123')
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'NoMatchingCourse: No Course has been found for a given id: 123'

    def test_get_course_query_returns_system_error_when_generic_exception_is_raised(self,
                                                                                    get_course_request):
        repo = Mock()
        repo.get_course.side_effect = Exception('System error.')
        query = GetCourseQuery(repo=repo)

        response = query.execute(request=get_course_request)

        repo.get_course.assert_called_with(course_id='123')
        assert isinstance(response, ResponseFailure)
        assert response.type == ResponseFailure.SYSTEM_ERROR
        assert response.message == 'Exception: System error.'
