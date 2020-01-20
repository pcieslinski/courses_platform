import json
import mock

from courses_platform.response_objects import ResponseSuccess
from courses_platform.serializers.json_course_serializer import CourseJsonEncoder


class TestUsersCoursesApi:

    @mock.patch('courses_platform.application.user.queries.get_user_courses.GetUserCoursesQuery')
    def test_users_courses_api_returns_list_of_user_courses(self, mock_query, client, courses):
        response = ResponseSuccess.build_response_success(courses)
        mock_query().execute.return_value = response

        http_response = client.get('/api/users/123/courses')
        courses_data = json.dumps(courses, cls=CourseJsonEncoder)

        assert json.loads(http_response.data.decode('UTF-8')) == json.loads(courses_data)
        assert mock_query().execute.call_count == 1
        assert http_response.status_code == 200
        assert http_response.mimetype == 'application/json'
