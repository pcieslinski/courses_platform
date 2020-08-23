import json
from typing import List

import pytest

from app.domain.user import User
from app.response_objects import ResponseSuccess, ResponseFailure


@pytest.fixture
def response_success(users: List[User]) -> ResponseSuccess:
    return ResponseSuccess('ResponseSuccess', users)


@pytest.fixture
def response_failure() -> ResponseFailure:
    return ResponseFailure('ResponseError', 'This is a response error')


class TestResponseSuccess:

    def test_response_success_initialize_correctly_with_value(self, response_success, users):
        assert isinstance(response_success, ResponseSuccess)
        assert response_success.type == 'ResponseSuccess'
        assert response_success.value is users

    def test_response_success_initialize_correctly_without_value(self):
        res = ResponseSuccess('ResponseSuccess')

        assert isinstance(res, ResponseSuccess)
        assert res.type == 'ResponseSuccess'
        assert res.value is None

    def test_response_success_is_true(self, response_success):
        assert bool(response_success) is True

    def test_response_success_builds_from_success_ok(self, users):
        res = ResponseSuccess.build_response_success(users)

        assert bool(res) is True
        assert isinstance(res, ResponseSuccess)
        assert res.type == ResponseSuccess.SUCCESS_OK
        assert res.value == users

    def test_response_success_builds_from_resource_created(self, users):
        res = ResponseSuccess.build_response_resource_created(users)

        assert bool(res) is True
        assert isinstance(res, ResponseSuccess)
        assert res.type == ResponseSuccess.SUCCESS_RESOURCE_CREATED
        assert res.value == users

    def test_response_success_builds_from_no_content(self):
        res = ResponseSuccess.build_response_no_content()

        assert bool(res) is True
        assert isinstance(res, ResponseSuccess)
        assert res.type == ResponseSuccess.SUCCESS_NO_CONTENT
        assert res.value == ''


class TestResponseFailure:

    def test_response_failure_initialize_correctly(self, response_failure):
        assert isinstance(response_failure, ResponseFailure)
        assert response_failure.type == 'ResponseError'
        assert response_failure.message == 'This is a response error'

    def test_response_failure_initialize_correctly_with_generic_exception(self):
        res = ResponseFailure('ResponseError', Exception('simple exception'))

        assert isinstance(res, ResponseFailure)
        assert res.type == 'ResponseError'
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
