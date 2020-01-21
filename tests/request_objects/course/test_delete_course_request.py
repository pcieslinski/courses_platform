from app.request_objects.course import DeleteCourseRequest


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
