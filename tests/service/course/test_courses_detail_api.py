import mock
from uuid import uuid4

from courses_platform.response_objects import ResponseSuccess


class TestCoursesDetailApi:

    @mock.patch('courses_platform.application.course.commands.delete.DeleteCourseCommand')
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
