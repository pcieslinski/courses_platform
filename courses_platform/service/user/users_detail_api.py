import json
from flask import Response
from flask_restful import Resource

from courses_platform.application.user.commands import delete
from courses_platform.application.interfaces.iuser_repository import URepository

from courses_platform.service.status_codes import STATUS_CODES
from courses_platform.request_objects.user import DeleteUserRequest


class UsersDetailApi(Resource):
    def __init__(self, repo: URepository) -> None:
        self.repo = repo

    def delete(self, user_id) -> Response:
        request_object = DeleteUserRequest.from_dict(dict(user_id=user_id))

        command = delete.DeleteUserCommand(repo=self.repo)

        response = command.execute(request=request_object)

        return Response(
            json.dumps(response.value),
            status=STATUS_CODES[response.type]
        )
