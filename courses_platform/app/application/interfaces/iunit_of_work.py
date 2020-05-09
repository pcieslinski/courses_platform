from __future__ import annotations
import abc
from typing import Any

from app.persistence.repositories import IRepository


class IUnitOfWork(abc.ABC):
    users: IRepository
    courses: IRepository

    @abc.abstractmethod
    def __enter__(self) -> IUnitOfWork:
        raise NotImplementedError

    @abc.abstractmethod
    def __exit__(self, *args: Any) -> None:
        raise NotImplementedError
