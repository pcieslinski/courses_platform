from app.request_objects.course import EnrollmentRequest


class TestEnrollmentRequest:

    def test_enrollment_request_initialize_correctly(self):
        req = EnrollmentRequest(course_id='100', user_id='20')

        assert isinstance(req, EnrollmentRequest)
        assert hasattr(req, 'course_id')
        assert hasattr(req, 'user_id')
        assert req.course_id == '100'
        assert req.user_id == '20'

    def test_enrollment_request_builds_correctly_from_dict(self):
        req = EnrollmentRequest.from_dict(dict(course_id='100', user_id='20'))

        assert isinstance(req, EnrollmentRequest)
        assert hasattr(req, 'course_id')
        assert hasattr(req, 'user_id')
        assert req.course_id == '100'
        assert req.user_id == '20'
