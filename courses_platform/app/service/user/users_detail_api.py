import json
from flask import Response
from flask_restful import Resource

from app.application.user.queries import get
from app.application.user.commands import delete
from app.application.interfaces.idb_session import DbSession

from app.serializers import UserJsonEncoder
from app.service.status_codes import STATUS_CODES
from app.request_objects.user import GetUserRequest, DeleteUserRequest


class UsersDetailApi(Resource):
    def __init__(self, db_session: DbSession) -> None:
        self.db_session = db_session

    def get(self, user_id: str) -> Response:
        request_object = GetUserRequest.from_dict(dict(user_id=user_id))

        query = get.GetUserQuery(db_session=self.db_session)

        response = query.execute(request=request_object)

        return Response(
            json.dumps(response.value, cls=UserJsonEncoder),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )

    def delete(self, user_id: str) -> Response:
        request_object = DeleteUserRequest.from_dict(dict(user_id=user_id))

        command = delete.DeleteUserCommand(db_session=self.db_session)

        response = command.execute(request=request_object)

        return Response(
            json.dumps(response.value),
            status=STATUS_CODES[response.type]
        )
