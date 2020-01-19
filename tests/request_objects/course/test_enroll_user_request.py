from courses_platform.request_objects import InvalidRequest
from courses_platform.request_objects.course import EnrollUserRequest


class TestEnrollUserRequest:

    def test_enroll_user_request_initialize_correctly(self):
        req = EnrollUserRequest(course_id='100', user_id='20')

        assert bool(req) is True
        assert isinstance(req, EnrollUserRequest)
        assert hasattr(req, 'course_id')
        assert hasattr(req, 'user_id')
        assert req.course_id == '100'
        assert req.user_id == '20'

    def test_enroll_user_request_builds_correctly_from_dict(self):
        req = EnrollUserRequest.from_dict(dict(course_id='100', user_id='20'))

        assert bool(req) is True
        assert isinstance(req, EnrollUserRequest)
        assert hasattr(req, 'course_id')
        assert hasattr(req, 'user_id')
        assert req.course_id == '100'
        assert req.user_id == '20'

    def test_enroll_user_request_returns_invalid_request_when_called_without_course_id(self):
        req = EnrollUserRequest.from_dict(dict(user_id='20'))

        assert isinstance(req, InvalidRequest)
        assert req.errors[0]['parameter'] == 'course_id'
        assert req.errors[0]['message'] == 'course_id is a required parameter'

    def test_enroll_user_request_returns_invalid_request_when_called_without_user_id(self):
        req = EnrollUserRequest.from_dict(dict(course_id='100'))

        assert isinstance(req, InvalidRequest)
        assert req.errors[0]['parameter'] == 'user_id'
        assert req.errors[0]['message'] == 'user_id is a required parameter'

    def test_enroll_user_request_returns_invalid_request_when_called_without_params(self):
        req = EnrollUserRequest.from_dict({})

        assert isinstance(req, InvalidRequest)
        assert req.errors[0]['parameter'] == 'course_id'
        assert req.errors[0]['message'] == 'course_id is a required parameter'
        assert req.errors[1]['parameter'] == 'user_id'
        assert req.errors[1]['message'] == 'user_id is a required parameter'
