import json
from flask import Response
from flask_restful import Resource

from app.application.interfaces.idb_session import DbSession
from app.application.course.commands import withdraw_user_enrollment as withdraw

from app.service.status_codes import STATUS_CODES
from app.request_objects.course import EnrollmentRequest


class EnrollmentsDetailApi(Resource):
    def __init__(self, db_session: DbSession) -> None:
        self.db_session = db_session

    def delete(self, course_id: str, user_id: str) -> Response:

        request_object = EnrollmentRequest.from_dict(
            {
                'course_id': course_id,
                'user_id': user_id
            }
        )

        command = withdraw.WithdrawUserEnrollmentCommand(db_session=self.db_session)

        response = command.execute(request=request_object)

        return Response(
            json.dumps(response.value),
            status=STATUS_CODES[response.type]
        )
