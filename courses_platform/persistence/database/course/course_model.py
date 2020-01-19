from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from courses_platform.persistence.database import Base
from courses_platform.persistence.database.enrollment_table import enrollment


class Course(Base):
    __tablename__ = 'course'

    id = Column(String(36),
                nullable=False,
                primary_key=True)
    name = Column(String(128),
                  nullable=False,
                  unique=True,
                  index=True)
    enrollments = relationship('User',
                               secondary=enrollment,
                               backref='courses',
                               lazy='dynamic')

    def __repr__(self) -> str:
        return f'<Course (id: {self.id}, name: {self.name})>'
