from courses_platform.response_objects.response_success import ResponseSuccess


class TestResponseSuccess:

    def test_response_success_initialize_correctly_with_value(self, users):
        res = ResponseSuccess(value=users)

        assert isinstance(res, ResponseSuccess)
        assert res.type == ResponseSuccess.SUCCESS
        assert res.value is users

    def test_response_success_initialize_correctly_without_value(self):
        res = ResponseSuccess()

        assert isinstance(res, ResponseSuccess)
        assert res.type == ResponseSuccess.SUCCESS
        assert res.value is None

    def test_response_success_is_true(self):
        assert bool(ResponseSuccess()) is True
