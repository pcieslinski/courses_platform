import json
from flask import Response
from flask_restful import Resource

from app.application.user.queries import get
from app.application.user.commands import delete
from app.application.interfaces.iunit_of_work import IUnitOfWork


from app.serializers import UserJsonEncoder
from app.service.status_codes import STATUS_CODES
from app.request_objects.user import GetUserRequest, DeleteUserRequest


class UsersDetailApi(Resource):
    def __init__(self, unit_of_work: IUnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    def get(self, user_id: str) -> Response:
        request_object = GetUserRequest.from_dict(dict(user_id=user_id))

        query = get.GetUserQuery(unit_of_work=self.unit_of_work)

        response = query.execute(request=request_object)

        return Response(
            json.dumps(response.value, cls=UserJsonEncoder),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )

    def delete(self, user_id: str) -> Response:
        request_object = DeleteUserRequest.from_dict(dict(user_id=user_id))

        command = delete.DeleteUserCommand(unit_of_work=self.unit_of_work)

        response = command.execute(request=request_object)

        return Response(
            json.dumps(response.value),
            status=STATUS_CODES[response.type]
        )
