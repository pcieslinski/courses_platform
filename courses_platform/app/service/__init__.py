from typing import Type, Tuple

from flask_restful import Api
from flask import Flask, jsonify

from app.service.extensions import ma
from app.service.config import Config, DevConfig
from app.service.user import UsersApi, UsersDetailApi, UsersCoursesApi
from app.service.course.views import (
    CoursesApi, CoursesDetailApi, EnrollmentsApi, EnrollmentsDetailApi)

from app.adapters import Session
from app.adapters.orm import start_mappers
from app.adapters.unit_of_work import SqlAlchemyUnitOfWork
from app.application.interfaces.iunit_of_work import IUnitOfWork


def create_app(config_object: Type[Config] = DevConfig) -> Flask:
    app = Flask(__name__)
    api = Api(app)

    ma.init_app(app)

    start_mappers()
    app.config.from_object(config_object)
    register_resources(api, SqlAlchemyUnitOfWork(session_factory=Session))

    @app.teardown_request
    def remove_session(exception: Exception = None) -> None:
        Session.remove()

    @app.errorhandler(422)
    def handle_error(err) -> Tuple[str, int]:
        messages = err.data.get("messages", ["Invalid request."])
        return jsonify({"errors": messages}), err.code

    return app


def register_resources(api: Api, unit_of_work: IUnitOfWork) -> None:
    api.add_resource(
        UsersApi,
        '/api/users',
        resource_class_kwargs={
            'unit_of_work': unit_of_work
        },
        endpoint='users'
    )
    api.add_resource(
        UsersDetailApi,
        '/api/users/<user_id>',
        resource_class_kwargs={
            'unit_of_work': unit_of_work
        },
        endpoint='user_details'
    )
    api.add_resource(
        UsersCoursesApi,
        '/api/users/<user_id>/courses',
        resource_class_kwargs={
            'unit_of_work': unit_of_work
        },
        endpoint='user_courses'
    )
    api.add_resource(
        CoursesApi,
        '/api/courses',
        resource_class_kwargs={
            'unit_of_work': unit_of_work
        },
        endpoint='courses'
    )
    api.add_resource(
        CoursesDetailApi,
        '/api/courses/<course_id>',
        resource_class_kwargs={
            'unit_of_work': unit_of_work
        },
        endpoint='course_details'
    )
    api.add_resource(
        EnrollmentsApi,
        '/api/courses/<course_id>/users',
        resource_class_kwargs={
            'unit_of_work': unit_of_work
        },
        endpoint='course_enrollment'
    )
    api.add_resource(
        EnrollmentsDetailApi,
        '/api/courses/<course_id>/users/<user_id>',
        resource_class_kwargs={
            'unit_of_work': unit_of_work
        },
        endpoint='course_enrollment_withdraw'
    )
