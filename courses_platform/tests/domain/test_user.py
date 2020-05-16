from app.domain.user import User
from app.domain.course import Course


class TestUserEntity:

    def test_user_initialize_correctly(self):
        user = User('test@gmail.com')

        assert isinstance(user, User)
        assert hasattr(user, 'id')

        assert user.email == 'test@gmail.com'
        assert user.courses == []

    def test_user_initialize_correctly_from_dict(self):
        user_dict = {
            'email': 'test@gmail.com'
        }

        user = User.from_dict(user_dict)

        assert isinstance(user, User)
        assert hasattr(user, 'id')

        assert user.email == 'test@gmail.com'
        assert user.courses == []

    def test_clear_enrollments_removes_all_user_enrollments(self):
        course_1 = Course(name='Test Course')
        course_2 = Course(name='Sample Course')
        user = User(email='test@gmail.com', courses=[course_1, course_2])

        user.clear_enrollments()

        assert user.courses == []
