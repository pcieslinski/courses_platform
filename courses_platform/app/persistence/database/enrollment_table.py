from sqlalchemy import Table, Column, String, ForeignKey

from app.persistence.database import Base


enrollment = Table(
    'enrollment',
    Base.metadata,
    Column('course_id', String(36), ForeignKey('course.id'), index=True),
    Column('user_id', String(36), ForeignKey('user.id'), index=True)
)
