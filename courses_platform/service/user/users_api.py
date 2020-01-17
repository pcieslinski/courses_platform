import json
from flask import Response, request
from flask_restful import Resource

from courses_platform.application.user.queries import get_all
from courses_platform.application.user.commands import create
from courses_platform.application.interfaces.iuser_repository import URepository

from courses_platform.service.status_codes import STATUS_CODES
from courses_platform.request_objects.user import CreateUserRequest
from courses_platform.serializers.json_user_serializer import UserJsonEncoder


class UsersApi(Resource):
    def __init__(self, repo: URepository) -> None:
        self.repo = repo

    def get(self) -> Response:
        query = get_all.GetAllUsersQuery(repo=self.repo)

        response = query.execute()

        return Response(
            json.dumps(response.value, cls=UserJsonEncoder),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )

    def post(self) -> Response:
        request_object = CreateUserRequest.from_dict(request.get_json())

        command = create.CreateUserCommand(repo=self.repo)

        response = command.execute(request=request_object)

        return Response(
            json.dumps(response.value, cls=UserJsonEncoder),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )
