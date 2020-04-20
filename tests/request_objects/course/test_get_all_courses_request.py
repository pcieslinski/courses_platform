from app.request_objects.course import GetAllCoursesRequest
from app.request_objects.invalid_request import InvalidRequest


class TestGetAllCoursesRequest:

    def test_get_all_courses_request_initialize_correctly(self):
        req = GetAllCoursesRequest(include=['stats'])

        assert isinstance(req, GetAllCoursesRequest)
        assert hasattr(req, 'include')
        assert isinstance(req.include, list)
        assert req.include[0] == 'stats'

    def test_get_all_courses_request_initialize_correctly_without_data(self):
        req = GetAllCoursesRequest()

        assert isinstance(req, GetAllCoursesRequest)
        assert hasattr(req, 'include')
        assert req.include == []

    def test_get_all_courses_request_builds_correctly_from_dict(self):
        req = GetAllCoursesRequest.from_dict(dict(include='stats'))

        assert isinstance(req, GetAllCoursesRequest)
        assert hasattr(req, 'include')
        assert isinstance(req.include, list)
        assert req.include[0] == 'stats'

    def test_get_all_courses_request_catches_errors_when_build_from_wrong_dict(self):
        req = GetAllCoursesRequest.from_dict(dict(include='stats,test'))

        assert isinstance(req, InvalidRequest)
        assert req.has_errors()
        assert req.errors[0]['parameter'] == 'test'
        assert req.errors[0]['message'] == 'test cannot be included with Courses'

    def test_get_all_courses_request_checks_acceptability_of_parameters(self):
        req = GetAllCoursesRequest.from_dict(dict(test='test'))

        assert isinstance(req, InvalidRequest)
        assert req.has_errors()
        assert req.errors[0]['parameter'] == 'test'
        assert req.errors[0]['message'] == 'test is not an acceptable parameter'
