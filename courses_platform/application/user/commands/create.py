from courses_platform.domain.user import User


class CreateUserCommand:
    def __init__(self, repo) -> None:
        self.repo = repo

    def execute(self, email: str) -> User:
        new_user = self.repo.create_user(email=email)
        return new_user
