from courses_platform.domain.user import User
from courses_platform.persistence.database import Session
from courses_platform.persistence.repositories.user import user_model as um


class UserRepository:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def create_user(self, email: str) -> User:
        with self.db_session() as db:
            user = User(email=email)

            db.add(
                um.User(
                    id=user.id,
                    email=user.email
                )
            )

            return user
