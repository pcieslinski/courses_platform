from courses_platform.request_objects import InvalidRequest
from courses_platform.request_objects.course import CreateCourseRequest


class TestCreateCourseRequest:

    def test_create_course_request_initialize_correctly(self):
        req = CreateCourseRequest(name='Test Course')

        assert bool(req) is True
        assert isinstance(req, CreateCourseRequest)
        assert hasattr(req, 'name')
        assert req.name == 'Test Course'

    def test_create_course_request_builds_correctly_from_dict(self):
        req = CreateCourseRequest.from_dict(dict(name='Test Course'))

        assert bool(req) is True
        assert isinstance(req, CreateCourseRequest)
        assert hasattr(req, 'name')
        assert req.name == 'Test Course'

    def test_from_dict_returns_invalid_request_when_called_with_not_string_type_name(self):
        req = CreateCourseRequest.from_dict(dict(name=100))

        assert isinstance(req, InvalidRequest)
        assert req.errors[0]['parameter'] == 'name'
        assert req.errors[0]['message'] == 'is not a string'
