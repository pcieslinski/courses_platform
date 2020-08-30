import abc
from typing import List, Literal, Union, Type

from sqlalchemy.orm import selectinload
from sqlalchemy.orm.session import Session

from app.domain.user import User
from app.domain.course import Course


Model = Union[Type[User], Type[Course]]
Entity = Union[User, Course]
Relationships = Literal['courses', 'enrollments']


class IRepository(abc.ABC):

    @abc.abstractmethod
    def add(self, entity: Entity):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, identifier: str, load_relation: Relationships = None) -> Entity:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> List[Entity]:
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, entity: Entity):
        raise NotImplementedError


class SqlAlchemyRepository(IRepository):
    """
    SQLAlchemy repository, which enables basic operations with the database
    and the selected model.

    Args:
        - session (sqlalchemy.orm.session.Session): Session object from sqlalchemy that enables
            communication with the database
        - model (Model): One of the classes that are used in the domain layer
    """

    def __init__(self, session: Session, model: Model):
        self.session = session
        self.model = model

    def add(self, entity: Entity) -> None:
        self.session.add(entity)

    def get(self, identifier: str, load_relation: Relationships = None) -> Entity:
        if load_relation:
            return self.session.query(self.model)\
                               .options(selectinload(load_relation))\
                               .filter_by(id=identifier)\
                               .first()

        return self.session.query(self.model)\
                           .filter_by(id=identifier)\
                           .first()

    def list(self) -> List[Entity]:
        return self.session.query(self.model).all()

    def remove(self, entity: Entity):
        self.session.delete(entity)
