from typing import Type, Tuple
from flask import Flask
from flask_restful import Api

from courses_platform.service.user.user_api import UserApi
from courses_platform.service.course.course_api import CourseApi
from courses_platform.service.config import Config, DevConfig

from courses_platform.application.interfaces.iuser_repository import URepository
from courses_platform.application.interfaces.icourse_repository import CRepository

from courses_platform.persistence.database import session
from courses_platform.persistence.repositories.user.user_repository import UserRepository
from courses_platform.persistence.repositories.course.course_repository import CourseRepository


def create_app(config_object: Type[Config] = DevConfig) -> Flask:
    app = Flask(__name__)
    api = Api(app)

    app.config.from_object(config_object)

    user_repo, course_repo = create_repositories()
    register_resources(api, user_repo, course_repo)

    return app


def register_resources(api: Api, user_repo: URepository, course_repo: CRepository) -> None:
    api.add_resource(
        UserApi,
        '/api/users',
        resource_class_kwargs={
            'repo': user_repo
        }
    )
    api.add_resource(
        CourseApi,
        '/api/courses',
        resource_class_kwargs={
            'repo': course_repo
        }
    )


def create_repositories() -> Tuple[URepository, CRepository]:
    user_repo = UserRepository(db_session=session)
    course_repo = CourseRepository(db_session=session)

    return user_repo, course_repo
