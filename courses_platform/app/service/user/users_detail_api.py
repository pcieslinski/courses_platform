from typing import List

from flask import Response
from flask_restful import Resource

from app.service.parser import use_kwargs
from app.application.user.queries import GetUserQuery
from app.application.user.commands import DeleteUserCommand
from app.service.status_codes import STATUS_CODES
from app.service.serializers import query_serializer
from app.service.serializers.schemas import UserSchema
from app.application.interfaces.iunit_of_work import IUnitOfWork


class UsersDetailApi(Resource):
    def __init__(self, unit_of_work: IUnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    @use_kwargs(query_serializer, location='querystring')
    def get(self, user_id: str, include: List[str] = None) -> Response:
        user_serializer = UserSchema(include=include)

        query = GetUserQuery(unit_of_work=self.unit_of_work)

        response = query.execute(user_id=user_id)

        return Response(
            response.serialize(user_serializer),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )

    def delete(self, user_id: str) -> Response:
        command = DeleteUserCommand(unit_of_work=self.unit_of_work)

        response = command.execute(user_id=user_id)

        return Response(
            response.serialize(),
            status=STATUS_CODES[response.type]
        )
