from courses_platform.request_objects import InvalidRequest
from courses_platform.request_objects.course import EnrollmentRequest


class TestEnrollmentRequest:

    def test_enrollment_request_initialize_correctly(self):
        req = EnrollmentRequest(course_id='100', user_id='20')

        assert bool(req) is True
        assert isinstance(req, EnrollmentRequest)
        assert hasattr(req, 'course_id')
        assert hasattr(req, 'user_id')
        assert req.course_id == '100'
        assert req.user_id == '20'

    def test_enrollment_request_builds_correctly_from_dict(self):
        req = EnrollmentRequest.from_dict(dict(course_id='100', user_id='20'))

        assert bool(req) is True
        assert isinstance(req, EnrollmentRequest)
        assert hasattr(req, 'course_id')
        assert hasattr(req, 'user_id')
        assert req.course_id == '100'
        assert req.user_id == '20'

    def test_enrollment_request_returns_invalid_request_when_called_without_course_id(self):
        req = EnrollmentRequest.from_dict(dict(user_id='20'))

        assert isinstance(req, InvalidRequest)
        assert req.errors[0]['parameter'] == 'course_id'
        assert req.errors[0]['message'] == 'course_id is a required parameter'

    def test_enrollment_request_returns_invalid_request_when_called_without_user_id(self):
        req = EnrollmentRequest.from_dict(dict(course_id='100'))

        assert isinstance(req, InvalidRequest)
        assert req.errors[0]['parameter'] == 'user_id'
        assert req.errors[0]['message'] == 'user_id is a required parameter'

    def test_enrollment_request_returns_invalid_request_when_called_without_params(self):
        req = EnrollmentRequest.from_dict({})

        assert isinstance(req, InvalidRequest)
        assert req.errors[0]['parameter'] == 'course_id'
        assert req.errors[0]['message'] == 'course_id is a required parameter'
        assert req.errors[1]['parameter'] == 'user_id'
        assert req.errors[1]['message'] == 'user_id is a required parameter'
