from typing import Type, Tuple
from flask import Flask
from flask_restful import Api

from courses_platform.service.config import Config, DevConfig
from courses_platform.service.user import UsersApi, UsersDetailApi
from courses_platform.service.course import CoursesApi, CoursesDetailApi, EnrollmentsApi

from courses_platform.persistence.database import session
from courses_platform.application.interfaces.idb_session import DbSession


def create_app(config_object: Type[Config] = DevConfig) -> Flask:
    app = Flask(__name__)
    api = Api(app)

    app.config.from_object(config_object)
    register_resources(api, session)

    return app


def register_resources(api: Api, db_session: DbSession) -> None:
    api.add_resource(
        UsersApi,
        '/api/users',
        resource_class_kwargs={
            'db_session': db_session
        }
    )
    api.add_resource(
        UsersDetailApi,
        '/api/users/<user_id>',
        resource_class_kwargs={
            'db_session': db_session
        }
    )
    api.add_resource(
        CoursesApi,
        '/api/courses',
        resource_class_kwargs={
            'db_session': db_session
        }
    )
    api.add_resource(
        CoursesDetailApi,
        '/api/courses/<course_id>',
        resource_class_kwargs={
            'db_session': db_session
        }
    )
    api.add_resource(
        EnrollmentsApi,
        '/api/courses/<course_id>/users',
        resource_class_kwargs={
            'db_session': db_session
        }
    )

