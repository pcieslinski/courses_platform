from app.domain.user import User


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
