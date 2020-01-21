import json
import mock
from uuid import uuid4

from app.response_objects import ResponseSuccess
from app.serializers.json_course_serializer import CourseJsonEncoder


class TestCoursesDetailApi:

    @mock.patch('app.application.course.queries.get.GetCourseQuery')
    def test_courses_detail_api_returns_course(self, mock_command, course, client):
        response = ResponseSuccess.build_response_success(course)
        mock_command().execute.return_value = response

        http_response = client.get('/api/courses/123')
        course_data = json.dumps(course, cls=CourseJsonEncoder)

        _, kwargs = mock_command().execute.call_args

        mock_command().execute.assert_called()
        assert kwargs['request'].course_id == '123'
        assert json.loads(http_response.data) == json.loads(course_data)
        assert http_response.status_code == 200

    @mock.patch('app.application.course.commands.delete.DeleteCourseCommand')
    def test_courses_detail_api_deletes_existing_course(self, mock_command, client):
        response = ResponseSuccess.build_response_no_content()
        mock_command().execute.return_value = response

        course_id = str(uuid4())
        http_response = client.delete(f'/api/courses/{course_id}')

        _, kwargs = mock_command().execute.call_args

        mock_command().execute.assert_called()
        assert kwargs['request'].course_id == course_id
        assert http_response.data == b''
        assert http_response.status_code == 204
