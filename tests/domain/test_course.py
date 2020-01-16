from uuid import uuid4

from courses_platform.domain.course import Course


class TestCourseEntity:

    def test_course_initialize_correctly(self):
        course = Course('Test Course')

        assert isinstance(course, Course)
        assert hasattr(course, 'id')

        assert course.name == 'Test Course'

    def test_course_initialize_correctly_from_dict(self):
        course_data = {
            'name': 'Test Course'
        }

        course = Course.from_dict(course_data)

        assert isinstance(course, Course)
        assert hasattr(course, 'id')

        assert course.name == 'Test Course'

    def test_course_initialize_correctly_form_record(self, course_record):
        course_id = str(uuid4())
        c_record = course_record(course_id, 'Test Course')

        course = Course.from_record(c_record)

        assert isinstance(course, Course)
        assert hasattr(course, 'id')

        assert course.id == course_id
        assert course.name == 'Test Course'
