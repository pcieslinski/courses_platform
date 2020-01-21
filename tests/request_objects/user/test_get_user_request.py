from app.request_objects.user import GetUserRequest


class TestGetUserRequest:

    def test_get_user_request_initialize_correctly(self):
        req = GetUserRequest(user_id='123')

        assert bool(req) is True
        assert isinstance(req, GetUserRequest)
        assert hasattr(req, 'user_id')
        assert req.user_id == '123'

    def test_get_user_request_builds_correctly_from_dict(self):
        req = GetUserRequest.from_dict(dict(user_id='123'))

        assert bool(req) is True
        assert isinstance(req, GetUserRequest)
        assert hasattr(req, 'user_id')
        assert req.user_id == '123'
