import json
import mock

from app.domain.course import Course
from app.serializers import CourseJsonEncoder
from app.response_objects import ResponseSuccess


class TestCoursesApi:

    @mock.patch('app.application.course.queries.get_all.GetAllCoursesQuery')
    def test_courses_api_returns_list_of_courses(self, mock_query, client):
        response_val = [Course('Test Course')]
        response = ResponseSuccess.build_response_success(response_val)
        mock_query().execute.return_value = response

        http_response = client.get('/api/courses')
        courses_data = json.dumps(response_val, cls=CourseJsonEncoder)

        assert json.loads(http_response.data.decode('UTF-8')) == json.loads(courses_data)
        assert mock_query().execute.call_count == 1
        assert http_response.status_code == 200
        assert http_response.mimetype == 'application/json'

    @mock.patch('app.application.course.queries.get_all.GetAllCoursesQuery')
    def test_courses_api_returns_list_of_courses_with_stats(self, mock_query, client,
                                                            courses_with_enrollments):
        response = ResponseSuccess.build_response_success(courses_with_enrollments)
        mock_query().execute.return_value = response

        http_response = client.get('/api/courses?include=stats')
        courses_data = json.dumps(courses_with_enrollments, cls=CourseJsonEncoder)

        _, kwargs = mock_query().execute.call_args

        assert json.loads(http_response.data.decode('UTF-8')) == json.loads(courses_data)
        assert mock_query().execute.call_count == 1
        assert kwargs['request'].include == ['stats']
        assert http_response.status_code == 200
        assert http_response.mimetype == 'application/json'

    @mock.patch('app.application.course.commands.create.CreateCourseCommand')
    def test_courses_api_creates_new_course(self, mock_command, client, course):
        response = ResponseSuccess.build_response_resource_created(course)
        mock_command().execute.return_value = response

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
        assert http_response.status_code == 201
        assert http_response.mimetype == 'application/json'
