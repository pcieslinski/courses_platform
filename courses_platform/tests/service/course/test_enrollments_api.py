import json
import mock

from app.response_objects import ResponseSuccess
from app.application.course.commands import EnrollUserCommand


class TestEnrollmentsApi:

    @mock.patch.object(EnrollUserCommand, 'execute')
    def test_enrollments_api_enrolls_user_for_course(self, mock_command, client):
        request_data = dict(course_id='123', user_id='1')
        response = ResponseSuccess.build_response_resource_created(request_data)
        mock_command.return_value = response

        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype
        }

        data = json.dumps(dict(user_id='1'))

        http_response = client.post('/api/courses/123/users', data=data, headers=headers)

        _, kwargs = mock_command.call_args

        assert json.loads(http_response.data.decode('UTF-8')) == request_data
        mock_command.assert_called()
        assert kwargs['course_id'] == '123'
        assert kwargs['user_id'] == '1'
        assert http_response.status_code == 201
        assert http_response.mimetype == 'application/json'
