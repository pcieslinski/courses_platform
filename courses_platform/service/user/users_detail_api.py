import json
from flask import Response
from flask_restful import Resource

from courses_platform.application.user.commands import delete
from courses_platform.application.interfaces.iuser_repository import URepository


class UsersDetailApi(Resource):
    def __init__(self, repo: URepository) -> None:
        self.repo = repo

    def delete(self, user_id) -> Response:
        command = delete.DeleteUserCommand(repo=self.repo)

        try:
            command.execute(user_id)

        except delete.NoMatchingUser:
            return Response(
                json.dumps({
                    'message': f'No User has been found for a given id: {user_id}'
                }),
                mimetype='application/json',
                status=404
            )

        return Response(
            json.dumps(''),
            status=204
        )
