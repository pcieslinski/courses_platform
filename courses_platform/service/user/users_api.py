import json
from flask import Response, request
from flask_restful import Resource

from courses_platform.application.user.queries import get_all
from courses_platform.application.user.commands import create
from courses_platform.serializers.json_user_serializer import UserJsonEncoder
from courses_platform.application.interfaces.iuser_repository import URepository


class UsersApi(Resource):
    def __init__(self, repo: URepository) -> None:
        self.repo = repo

    def get(self) -> Response:
        query = get_all.GetAllUsersQuery(repo=self.repo)

        result = query.execute()

        return Response(
            json.dumps(result, cls=UserJsonEncoder),
            mimetype='application/json',
            status=200
        )

    def post(self) -> Response:
        req_data = request.get_json()

        command = create.CreateUserCommand(repo=self.repo)

        result = command.execute(req_data['email'])

        return Response(
            json.dumps(result, cls=UserJsonEncoder),
            mimetype='application/json',
            status=201
        )
