import pytest

from app.request_objects import ValidRequest, InvalidRequest


class TestValidRequest:

    def test_valid_request_raises_error_when_built_from_dict(self):
        with pytest.raises(NotImplementedError):
            ValidRequest.from_dict({})

    def test_validate_required_params_validates_parameters(self):
        ValidRequest.required_params = ('name', )

        invalid_req = ValidRequest.validate_required_params(
            invalid_req=InvalidRequest(),
            params=dict(email='test')
        )

        assert invalid_req.has_errors()
        assert invalid_req.errors[0]['parameter'] == 'name'
        assert invalid_req.errors[0]['message'] == 'name is a required parameter'

    def test_validate_accepted_params_validates_parameters(self):
        ValidRequest.accepted_params = ('include', )

        invalid_req = ValidRequest.validate_accepted_params(
            invalid_req=InvalidRequest(),
            params=dict(test='test')
        )

        assert invalid_req.has_errors()
        assert invalid_req.errors[0]['parameter'] == 'test'
        assert invalid_req.errors[0]['message'] == 'test is not an acceptable parameter'
