from typing import List

from courses_platform.domain.user import User
from courses_platform.persistence.database import Session
from courses_platform.persistence.repositories.user import user_model as um
from courses_platform.application.interfaces.iuser_repository import IUserRepository


class UserRepository(IUserRepository):
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

    def delete_user(self, user_id: str) -> bool:
        with self.db_session() as db:
            result = db.query(um.User).\
                        filter(um.User.id == user_id).\
                        delete()

            return result

    def get_user(self, user_id: str) -> User:
        with self.db_session() as db:
            result = db.query(um.User).\
                        filter(um.User.id == user_id).\
                        first()

            return User.from_record(result)

    def get_all_users(self) -> List[User]:
        with self.db_session() as db:
            result = db.query(um.User).\
                        all()

            users = [
                User.from_record(user_record)
                for user_record in result
            ]

            return users
