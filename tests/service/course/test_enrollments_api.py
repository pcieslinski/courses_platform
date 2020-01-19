import json
import mock

from courses_platform.response_objects import ResponseSuccess


class TestEnrollmentsApi:

    @mock.patch('courses_platform.application.course.commands.enroll_user.EnrollUserCommand')
    def test_enrollments_api_enrolls_user_for_course(self, mock_command, client):
        request_data = dict(course_id='123', user_id='1')
        response = ResponseSuccess.build_response_resource_created(request_data)
        mock_command().execute.return_value = response

        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype
        }

        data = json.dumps(dict(user_id='1'))

        http_response = client.post('/api/courses/123/users', data=data, headers=headers)

        _, kwargs = mock_command().execute.call_args

        assert json.loads(http_response.data.decode('UTF-8')) == request_data
        mock_command().execute.assert_called()
        assert kwargs['request'].course_id == '123'
        assert kwargs['request'].user_id == '1'
        assert http_response.status_code == 201
        assert http_response.mimetype == 'application/json'
