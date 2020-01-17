from courses_platform.request_objects import InvalidRequest
from courses_platform.request_objects.user import DeleteUserRequest


class TestDeleteUserRequest:

    def test_delete_user_request_initialize_correctly(self):
        req = DeleteUserRequest(user_id='123')

        assert bool(req) is True
        assert isinstance(req, DeleteUserRequest)
        assert hasattr(req, 'user_id')
        assert req.user_id == '123'

    def test_delete_user_request_builds_correctly_from_dict(self):
        req = DeleteUserRequest.from_dict(dict(user_id='123'))

        assert bool(req) is True
        assert isinstance(req, DeleteUserRequest)
        assert hasattr(req, 'user_id')
        assert req.user_id == '123'

    def test_from_dict_returns_invalid_request_when_called_without_user_id(self):
        req = DeleteUserRequest.from_dict({})

        assert isinstance(req, InvalidRequest)
        assert req.errors[0]['parameter'] == 'user_id'
        assert req.errors[0]['message'] == 'user_id is a required parameter'
