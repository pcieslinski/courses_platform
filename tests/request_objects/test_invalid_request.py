import pytest

from courses_platform.request_objects import InvalidRequest


@pytest.fixture
def invalid_request():
    return InvalidRequest()


class TestInvalidRequest:

    def test_invalid_request_initialize_correctly(self, invalid_request):
        assert isinstance(invalid_request, InvalidRequest)
        assert invalid_request.errors == []

    def test_add_error_adds_error_to_invalid_request(self, invalid_request):
        invalid_request.add_error(
            parameter='email',
            message='email is a required parameter'
        )

        assert len(invalid_request.errors) == 1
        assert invalid_request.errors[0]['parameter'] == 'email'
        assert invalid_request.errors[0]['message'] == 'email is a required parameter'

    def test_has_errors_returns_true_when_called_with_invalid_request_with_errors(self,
                                                                                  invalid_request):
        invalid_request.add_error(
            parameter='email',
            message='email is a required parameter'
        )

        assert invalid_request.has_errors()

    def test_has_errors_returns_false_when_called_with_invalid_request_without_errors(self,
                                                                                      invalid_request):
        assert not invalid_request.has_errors()

    def test_invalid_request_is_false(self, invalid_request):
        assert bool(invalid_request) is False
