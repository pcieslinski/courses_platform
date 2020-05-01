from typing import Type

from flask import Flask
from flask_restful import Api

from app.service.config import Config, DevConfig
from app.service.user import UsersApi, UsersDetailApi, UsersCoursesApi
from app.service.course import (
    CoursesApi, CoursesDetailApi, EnrollmentsApi, EnrollmentsDetailApi)

from app.persistence import session, Session
from app.persistence.orm import start_mappers
from app.application.interfaces.idb_session import DbSession


def create_app(config_object: Type[Config] = DevConfig) -> Flask:
    app = Flask(__name__)
    api = Api(app)

    start_mappers()
    app.config.from_object(config_object)
    register_resources(api, session)

    @app.teardown_request
    def remove_session(exception: Exception = None) -> None:
        Session.remove()

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
        UsersCoursesApi,
        '/api/users/<user_id>/courses',
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
    api.add_resource(
        EnrollmentsDetailApi,
        '/api/courses/<course_id>/users/<user_id>',
        resource_class_kwargs={
            'db_session': db_session
        }
    )
