import pytest

from courses_platform.request_objects.valid_request import ValidRequest


class TestValidRequest:

    def test_valid_request_raises_error_when_built_from_dict(self):
        with pytest.raises(NotImplementedError):
            req = ValidRequest.from_dict({})

    def test_valid_request_is_true(self):
        req = ValidRequest()

        assert bool(req) is True
