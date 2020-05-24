from flask import Response
from flask_restful import Resource

from app.service.parser import use_kwargs
from app.application.user.queries import get_all
from app.application.user.commands import create
from app.service.status_codes import STATUS_CODES
from app.application.interfaces.iunit_of_work import IUnitOfWork
from app.service.serializers import user_serializer, users_serializer


class UsersApi(Resource):
    def __init__(self, unit_of_work: IUnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    def get(self) -> Response:
        query = get_all.GetAllUsersQuery(unit_of_work=self.unit_of_work)

        response = query.execute()

        return Response(
            response.serialize(users_serializer),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )

    @use_kwargs(user_serializer)
    def post(self, email: str) -> Response:
        command = create.CreateUserCommand(unit_of_work=self.unit_of_work)

        response = command.execute(email=email)

        return Response(
            response.serialize(user_serializer),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )
