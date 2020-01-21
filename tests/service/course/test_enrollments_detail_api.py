import mock

from app.response_objects import ResponseSuccess


class TestEnrollmentsDetailApi:

    @mock.patch('app.application.course.commands.withdraw_user_enrollment.WithdrawUserEnrollmentCommand')
    def test_enrollments_detail_api_withdraws_user_enrollment(self, mock_command, client):
        response = ResponseSuccess.build_response_no_content()
        mock_command().execute.return_value = response

        http_response = client.delete('/api/courses/123/users/20')

        _, kwargs = mock_command().execute.call_args

        mock_command().execute.assert_called()
        assert kwargs['request'].course_id == '123'
        assert kwargs['request'].user_id == '20'
        assert http_response.data == b''
        assert http_response.status_code == 204
