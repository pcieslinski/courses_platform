from flask import Response
from flask_restful import Resource

from app.serializers import user_serializer
from app.application.user.queries import get
from app.application.user.commands import delete
from app.service.status_codes import STATUS_CODES
from app.application.interfaces.iunit_of_work import IUnitOfWork


class UsersDetailApi(Resource):
    def __init__(self, unit_of_work: IUnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    def get(self, user_id: str) -> Response:
        query = get.GetUserQuery(unit_of_work=self.unit_of_work)

        response = query.execute(user_id=user_id)

        return Response(
            response.serialize(user_serializer),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )

    def delete(self, user_id: str) -> Response:
        command = delete.DeleteUserCommand(unit_of_work=self.unit_of_work)

        response = command.execute(user_id=user_id)

        return Response(
            response.serialize(),
            status=STATUS_CODES[response.type]
        )
