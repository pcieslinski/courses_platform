import click
from uuid import uuid4

from courses_platform.persistence.database.user import User
from courses_platform.persistence.database.course import Course
from courses_platform.persistence.database.enrollment_table import enrollment
from courses_platform.persistence.database import Base, engine, session


@click.group()
def main():
    pass


@main.command()
def create_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@main.command()
def seed_db():
    with session() as db:
        users = [
            User(id=str(uuid4()), email='test@gmail'),
            User(id=str(uuid4()), email='sample@gmail'),
            User(id=str(uuid4()), email='random@gmail'),
            User(id=str(uuid4()), email='default@gmail')
        ]

        courses = [
            Course(id=str(uuid4()), name='Test Course'),
            Course(id=str(uuid4()), name='Sample Course')
        ]

        db.bulk_save_objects(users)
        db.bulk_save_objects(courses)

        db_courses = db.query(Course).all()
        db_users = db.query(User).all()

        db_courses[0].enrollments.append(db_users[0])
        db_courses[0].enrollments.append(db_users[1])
        db_courses[1].enrollments.append(db_users[1])
        db_courses[1].enrollments.append(db_users[2])


if __name__ == "__main__":
    main()
