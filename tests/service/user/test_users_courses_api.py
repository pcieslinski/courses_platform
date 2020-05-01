import json
import mock

from app.domain.course import Course
from app.serializers import CourseJsonEncoder
from app.response_objects import ResponseSuccess


class TestUsersCoursesApi:

    @mock.patch('app.application.user.queries.get_user_courses.GetUserCoursesQuery')
    def test_users_courses_api_returns_list_of_user_courses(self, mock_query, client):
        response_val = [Course('Test Course')]
        response = ResponseSuccess.build_response_success(response_val)
        mock_query().execute.return_value = response

        http_response = client.get('/api/users/123/courses')
        courses_data = json.dumps(response_val, cls=CourseJsonEncoder)

        assert json.loads(http_response.data.decode('UTF-8')) == json.loads(courses_data)
        assert mock_query().execute.call_count == 1
        assert http_response.status_code == 200
        assert http_response.mimetype == 'application/json'
