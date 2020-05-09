import json
from flask import Response, request
from flask_restful import Resource

from app.application.user.queries import get_all
from app.application.user.commands import create
from app.application.interfaces.iunit_of_work import IUnitOfWork

from app.serializers import UserJsonEncoder
from app.service.status_codes import STATUS_CODES
from app.request_objects.user import CreateUserRequest


class UsersApi(Resource):
    def __init__(self, unit_of_work: IUnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    def get(self) -> Response:
        query = get_all.GetAllUsersQuery(unit_of_work=self.unit_of_work)

        response = query.execute()

        return Response(
            json.dumps(response.value, cls=UserJsonEncoder),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )

    def post(self) -> Response:
        request_object = CreateUserRequest.from_dict(request.get_json())

        command = create.CreateUserCommand(unit_of_work=self.unit_of_work)

        response = command.execute(request=request_object)

        return Response(
            json.dumps(response.value, cls=UserJsonEncoder),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )
