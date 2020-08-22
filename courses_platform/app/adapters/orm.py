from sqlalchemy.orm import mapper, relationship
from sqlalchemy import Column, ForeignKey, MetaData, String, Table

from app.domain.user import User
from app.domain.course import Course


metadata: MetaData = MetaData()


user: Table = Table(
    'user', metadata,
    Column('id',
           String(36),
           primary_key=True),
    Column('email',
           String(72),
           nullable=False,
           unique=True,
           index=True)
)

course: Table = Table(
    'course', metadata,
    Column('id',
           String(36),
           primary_key=True),
    Column('name',
           String(128),
           nullable=False,
           index=True),
)

enrollment: Table = Table(
    'enrollment', metadata,
    Column(
        'course_id',
        String(36),
        ForeignKey('course.id'),
        index=True),
    Column(
        'user_id',
        String(36),
        ForeignKey('user.id'),
        index=True)
)


def start_mappers() -> None:
    users_mapper = mapper(User, user)
    mapper(
        Course, course, properties={
            'enrollments': relationship(
                users_mapper,
                secondary=enrollment,
                backref='courses',
                lazy='dynamic'

            )
        }
    )
