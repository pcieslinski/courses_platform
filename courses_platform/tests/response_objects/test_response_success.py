from typing import List

import pytest

from app.domain.user import User
from app.response_objects import ResponseSuccess


@pytest.fixture
def response_type() -> str:
    return 'ResponseSuccess'


@pytest.fixture
def response_value(users: List[User]) -> List[User]:
    return users


@pytest.fixture
def response_success(response_type: str, response_value: List[User]) -> ResponseSuccess:
    return ResponseSuccess(response_type, response_value)


class TestResponseSuccess:

    def test_response_success_initialize_correctly_with_value(self, response_success, users):
        assert isinstance(response_success, ResponseSuccess)
        assert response_success.type == 'ResponseSuccess'
        assert response_success.value is users

    def test_response_success_initialize_correctly_without_value(self, response_type):
        res = ResponseSuccess(response_type)

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
