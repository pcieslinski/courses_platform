from app.domain.user import User
from app.domain.course import Course


class TestCourseEntity:

    def test_course_initialize_correctly(self):
        course = Course('Test Course')

        assert isinstance(course, Course)
        assert hasattr(course, 'id')

        assert course.name == 'Test Course'
        assert course.enrollments == []

    def test_course_initialize_correctly_from_dict(self):
        course_data = {
            'name': 'Test Course'
        }

        course = Course.from_dict(course_data)

        assert isinstance(course, Course)
        assert hasattr(course, 'id')

        assert course.name == 'Test Course'
        assert course.enrollments == []

    def test_enrollments_count_property_returns_number_of_enrollments(self):
        course = Course(name='Test Course', enrollments=[
            User(email='test@gmail.com')
        ])

        assert course.enrollments_count == 1

    def test_enroll_method_enrolls_user_to_the_course(self):
        user = User(email='test@gmail.com')
        course = Course(name='Test Course')

        course.enroll(user)

        assert course.is_enrolled(user)

    def test_withdraw_enrollment_method_withdraws_user_enrollment(self):
        user = User(email='test@gmail.com')
        course = Course(name='Test Course', enrollments=[user])

        course.withdraw_enrollment(user)

        assert not course.is_enrolled(user)

    def test_is_enrolled_checks_if_user_is_enrolled_in_course(self):
        user = User(email='test@gmail.com')
        course = Course(name='Test Course', enrollments=[user])

        assert course.is_enrolled(user)

    def test_clear_enrollments_removes_all_enrollments_for_a_course(self):
        user_1 = User('test@gmail.com')
        user_2 = User('dev@gmail.com')
        course = Course(name='Test Course', enrollments=[user_1, user_2])

        course.clear_enrollments()

        assert course.enrollments == []
