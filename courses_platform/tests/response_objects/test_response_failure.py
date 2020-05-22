import json
import pytest

from app.response_objects import ResponseFailure


@pytest.fixture
def response_type() -> str:
    return 'ResponseError'


@pytest.fixture
def response_message() -> str:
    return 'This is a response error'


@pytest.fixture
def response_failure(response_type, response_message) -> ResponseFailure:
    return ResponseFailure(response_type, response_message)


class TestResponseFailure:

    def test_response_failure_initialize_correctly(self, response_failure):
        assert isinstance(response_failure, ResponseFailure)
        assert response_failure.type == 'ResponseError'
        assert response_failure.message == 'This is a response error'

    def test_response_failure_initialize_correctly_with_generic_exception(self, response_type):
        res = ResponseFailure(response_type, Exception('simple exception'))

        assert isinstance(res, ResponseFailure)
        assert res.type == response_type
        assert res.message == 'Exception: simple exception'

    def test_property_value_returns_response_type_and_message(self, response_failure):
        assert response_failure.value == {
            'type': 'ResponseError',
            'message': 'This is a response error'
        }

    def test_response_failure_is_false(self, response_failure):
        assert bool(response_failure) is False

    def test_response_failure_builds_from_resource_error(self):
        res = ResponseFailure.build_resource_error(Exception('resource error'))

        assert bool(res) is False
        assert isinstance(res, ResponseFailure)
        assert res.type == ResponseFailure.RESOURCE_ERROR
        assert res.message == 'Exception: resource error'

    def test_response_failure_builds_from_system_error(self):
        res = ResponseFailure.build_system_error(Exception('system error'))

        assert bool(res) is False
        assert isinstance(res, ResponseFailure)
        assert res.type == ResponseFailure.SYSTEM_ERROR
        assert res.message == 'Exception: system error'

    def test_response_failure_builds_from_parameters_error(self):
        res = ResponseFailure.build_parameters_error(Exception('parameter error'))

        assert bool(res) is False
        assert isinstance(res, ResponseFailure)
        assert res.type == ResponseFailure.PARAMETERS_ERROR
        assert res.message == 'Exception: parameter error'

    def test_response_failure_serializes_correctly(self, response_failure):
        serialized_res = response_failure.serialize()

        expected = dict(
            message='This is a response error',
            type='ResponseError'
        )

        assert json.loads(serialized_res) == expected
