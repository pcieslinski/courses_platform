from uuid import uuid4

from courses_platform.domain.user import User


class TestUserEntity:

    def test_user_initialize_correctly(self):
        user = User('test@gmail.com')

        assert isinstance(user, User)
        assert hasattr(user, 'id')

        assert user.email == 'test@gmail.com'

    def test_user_initialize_correctly_from_dict(self):
        user_dict = {
            'email': 'test@gmail.com'
        }

        user = User.from_dict(user_dict)

        assert isinstance(user, User)
        assert hasattr(user, 'id')

        assert user.email == 'test@gmail.com'

    def test_user_initialize_correctly_from_record(self):
        user_id = str(uuid4())
        user_record = {
            'id': user_id,
            'email': 'test@gmail.com'
        }

        user = User.from_record(user_record)

        assert isinstance(user, User)
        assert hasattr(user, 'id')

        assert user.id == user_id
        assert user.email == 'test@gmail.com'
