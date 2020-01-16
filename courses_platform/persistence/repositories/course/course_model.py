from sqlalchemy import Column, String

from courses_platform.persistence.database import Base


class Course(Base):
    __tablename__ = 'course'

    id = Column(String(36),
                nullable=False,
                primary_key=True)
    name = Column(String(128),
                  nullable=False,
                  unique=True,
                  index=True)

    def __repr__(self) -> str:
        return f'<Course (id: {self.id}, name: {self.name})>'
