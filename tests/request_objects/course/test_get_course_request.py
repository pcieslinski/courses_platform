from app.request_objects.course import GetCourseRequest


class TestGetCourseRequest:

    def test_get_course_request_initialize_correctly(self):
        req = GetCourseRequest(course_id='100')

        assert bool(req) is True
        assert isinstance(req, GetCourseRequest)
        assert hasattr(req, 'course_id')
        assert req.course_id == '100'

    def test_get_course_request_builds_correctly_from_dict(self):
        req = GetCourseRequest.from_dict(dict(course_id='100'))

        assert bool(req) is True
        assert isinstance(req, GetCourseRequest)
        assert hasattr(req, 'course_id')
        assert req.course_id == '100'
