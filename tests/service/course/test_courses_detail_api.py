import mock
from uuid import uuid4


class TestCoursesDetailApi:

    @mock.patch('courses_platform.application.course.commands.delete.DeleteCourseCommand')
    def test_courses_detail_api_deletes_existing_course(self, mock_command, client):
        mock_command().execute.return_value = 1

        course_id = str(uuid4())
        http_response = client.delete(f'/api/courses/{course_id}')

        mock_command().execute.assert_called_with(course_id)
        assert http_response.json is None
        assert http_response.status_code == 204

    @mock.patch('courses_platform.application.course.commands.delete.DeleteCourseCommand')
    def test_courses_detail_api_raises_error_when_deletes_not_existing_course(self, mock_command, client):
        mock_command().execute.side_effect = Exception

        http_response = client.delete('/api/courses/bad_id')

        mock_command().execute.assert_called_with('bad_id')
        assert http_response.json['message'] == 'No Course has been found for a given id: bad_id'
        assert http_response.status_code == 404
        assert http_response.mimetype == 'application/json'
