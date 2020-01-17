from courses_platform.request_objects import InvalidRequest
from courses_platform.request_objects.course import DeleteCourseRequest


class TestDeleteCourseRequest:

    def test_delete_course_request_initialize_correctly(self):
        req = DeleteCourseRequest(course_id='100')

        assert bool(req) is True
        assert isinstance(req, DeleteCourseRequest)
        assert hasattr(req, 'course_id')
        assert req.course_id == '100'

    def test_delete_course_request_builds_correctly_from_dict(self):
        req = DeleteCourseRequest.from_dict(dict(course_id='100'))

        assert bool(req) is True
        assert isinstance(req, DeleteCourseRequest)
        assert hasattr(req, 'course_id')
        assert req.course_id == '100'

    def test_from_dict_returns_invalid_request_when_called_without_course_id(self):
        req = DeleteCourseRequest.from_dict({})

        assert isinstance(req, InvalidRequest)
        assert req.errors[0]['parameter'] == 'course_id'
        assert req.errors[0]['message'] == 'course_id is a required parameter'
