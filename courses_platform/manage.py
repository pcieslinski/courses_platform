import click

from app.domain.user import User
from app.domain.course import Course
from app.persistence import engine, Session
from app.persistence.orm import metadata, start_mappers
from app.persistence.unit_of_work import SqlAlchemyUnitOfWork


@click.group()
def main():
    pass


@main.command()
def create_db():
    metadata.drop_all(bind=engine)
    metadata.create_all(bind=engine)


@main.command()
def seed_db():
    start_mappers()

    unit_of_work = SqlAlchemyUnitOfWork(session_factory=Session)

    with unit_of_work as uow:
        users = [
            User(email='test@gmail'),
            User(email='sample@gmail'),
            User(email='random@gmail'),
            User(email='default@gmail')
        ]

        courses = [
            Course(name='Test Course'),
            Course(name='Sample Course')
        ]

        courses[0].enrollments.append(users[0])
        courses[0].enrollments.append(users[1])
        courses[1].enrollments.append(users[1])
        courses[1].enrollments.append(users[2])

        for user in users:
            uow.users.add(user)

        for course in courses:
            uow.courses.add(course)

    Session.remove()


if __name__ == "__main__":
    main()
