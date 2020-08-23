from typing import List

from flask import Response
from flask_restful import Resource

from app.application.user import queries
from app.application.user import commands
from app.service.parser import use_kwargs
from app.service.status_codes import STATUS_CODES
from app.service.schemas import query_serializer
from app.service.course.serializers import courses_serializer
from app.service.user.serializers import UserSchema, user_serializer
from app.application.interfaces.iunit_of_work import IUnitOfWork


class UsersApi(Resource):
    def __init__(self, unit_of_work: IUnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    @use_kwargs(query_serializer, location='querystring')
    def get(self, include: List[str] = None) -> Response:
        users_serializer = UserSchema(many=True, include=include)

        query = queries.GetAllUsersQuery(unit_of_work=self.unit_of_work)

        response = query.execute()

        return Response(
            response.serialize(users_serializer),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )

    @use_kwargs(user_serializer)
    def post(self, email: str) -> Response:
        command = commands.CreateUserCommand(unit_of_work=self.unit_of_work)

        response = command.execute(email=email)

        return Response(
            response.serialize(user_serializer),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )


class UsersDetailApi(Resource):
    def __init__(self, unit_of_work: IUnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    @use_kwargs(query_serializer, location='querystring')
    def get(self, user_id: str, include: List[str] = None) -> Response:
        user_serializer = UserSchema(include=include)

        query = queries.GetUserQuery(unit_of_work=self.unit_of_work)

        response = query.execute(user_id=user_id)

        return Response(
            response.serialize(user_serializer),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )

    def delete(self, user_id: str) -> Response:
        command = commands.DeleteUserCommand(unit_of_work=self.unit_of_work)

        response = command.execute(user_id=user_id)

        return Response(
            response.serialize(),
            status=STATUS_CODES[response.type]
        )


class UsersCoursesApi(Resource):
    def __init__(self, unit_of_work: IUnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    def get(self, user_id: str) -> Response:
        query = queries.GetUserCoursesQuery(unit_of_work=self.unit_of_work)

        response = query.execute(user_id=user_id)

        return Response(
            response.serialize(courses_serializer),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )
