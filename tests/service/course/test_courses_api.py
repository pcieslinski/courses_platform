import json
import mock

from courses_platform.response_objects import ResponseSuccess
from courses_platform.serializers.json_course_serializer import CourseJsonEncoder


class TestCoursesApi:

    @mock.patch('courses_platform.application.course.queries.get_all.GetAllCoursesQuery')
    def test_courses_api_returns_list_of_courses(self, mock_query, client, courses):
        mock_query().execute.return_value = ResponseSuccess(value=courses)

        http_response = client.get('/api/courses')
        courses_data = json.dumps(courses, cls=CourseJsonEncoder)

        assert json.loads(http_response.data.decode('UTF-8')) == json.loads(courses_data)
        mock_query().execute.assert_called_with()
        assert http_response.status_code == 200
        assert http_response.mimetype == 'application/json'

    @mock.patch('courses_platform.application.course.queries.get_all.GetAllCoursesQuery')
    def test_courses_api_returns_empty_list_of_courses(self, mock_query, client):
        mock_query().execute.return_value = ResponseSuccess(value=[])

        http_response = client.get('/api/courses')

        assert json.loads(http_response.data.decode('UTF-8')) == []
        mock_query().execute.assert_called_with()
        assert http_response.status_code == 200
        assert http_response.mimetype == 'application/json'

    @mock.patch('courses_platform.application.course.commands.create.CreateCourseCommand')
    def test_courses_api_creates_new_course(self, mock_command, client, course):
        mock_command().execute.return_value = ResponseSuccess(value=course)

        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype
        }

        data = json.dumps(dict(name='Test Course'))

        http_response = client.post('/api/courses', data=data, headers=headers)
        course_data = json.dumps(course, cls=CourseJsonEncoder)

        _, kwargs = mock_command().execute.call_args

        assert json.loads(http_response.data.decode('UTF-8')) == json.loads(course_data)
        mock_command().execute.assert_called()
        assert kwargs['request'].name == 'Test Course'
        assert http_response.status_code == 200
        assert http_response.mimetype == 'application/json'
