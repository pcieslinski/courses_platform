import mock

from app.response_objects import ResponseSuccess
from app.application.course.commands import WithdrawUserEnrollmentCommand


class TestEnrollmentsDetailApi:

    @mock.patch.object(WithdrawUserEnrollmentCommand, 'execute')
    def test_enrollments_detail_api_withdraws_user_enrollment(self, mock_command, client):
        response = ResponseSuccess.build_response_no_content()
        mock_command.return_value = response

        http_response = client.delete('/api/courses/123/users/20')

        _, kwargs = mock_command.call_args

        mock_command.assert_called()
        assert kwargs['course_id'] == '123'
        assert kwargs['user_id'] == '20'
        assert http_response.data == b''
        assert http_response.status_code == 204
