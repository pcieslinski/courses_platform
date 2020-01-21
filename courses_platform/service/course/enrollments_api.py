import json
from flask import Response, request
from flask_restful import Resource

from courses_platform.application.course.commands import enroll_user
from courses_platform.application.interfaces.idb_session import DbSession

from courses_platform.service.status_codes import STATUS_CODES
from app.request_objects.course import EnrollmentRequest


class EnrollmentsApi(Resource):
    def __init__(self, db_session: DbSession) -> None:
        self.db_session = db_session

    def post(self, course_id: str) -> Response:
        params = request.get_json()

        request_object = EnrollmentRequest.from_dict(
            {
                'course_id': course_id,
                'user_id': params['user_id']
            }
        )

        command = enroll_user.EnrollUserCommand(db_session=self.db_session)

        response = command.execute(request=request_object)

        return Response(
            json.dumps(response.value),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )
