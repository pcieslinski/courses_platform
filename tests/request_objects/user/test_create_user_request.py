from app.request_objects.invalid_request import InvalidRequest
from app.request_objects.user import CreateUserRequest


class TestCreateUserRequest:

    def test_create_user_request_initialize_correctly(self):
        req = CreateUserRequest(email='test@gmail.com')

        assert isinstance(req, CreateUserRequest)
        assert hasattr(req, 'email')
        assert req.email == 'test@gmail.com'

    def test_create_user_request_builds_correctly_from_dict(self):
        req = CreateUserRequest.from_dict(dict(email='test@gmail.com'))

        assert isinstance(req, CreateUserRequest)
        assert hasattr(req, 'email')
        assert req.email == 'test@gmail.com'

    def test_from_dict_returns_invalid_request_when_called_with_not_string_type_email(self):
        req = CreateUserRequest.from_dict(dict(email=1))

        assert isinstance(req, InvalidRequest)
        assert req.errors[0]['parameter'] == 'email'
        assert req.errors[0]['message'] == 'is not a string'
