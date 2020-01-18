import abc
from typing import List, NewType

from courses_platform.domain.user import User


class IUserRepository(abc.ABC):

    @abc.abstractmethod
    def create_user(self, email: str) -> User:
        pass

    @abc.abstractmethod
    def delete_user(self, user_id: str) -> bool:
        pass

    @abc.abstractmethod
    def get_user(self, user_id: str) -> User:
        pass

    @abc.abstractmethod
    def get_all_users(self) -> List[User]:
        pass


URepository = NewType('URepository', IUserRepository)
