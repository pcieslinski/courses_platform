from flask import Response, request
from flask_restful import Resource

from app.application.course.commands import enroll_user
from app.application.interfaces.iunit_of_work import IUnitOfWork

from app.service.status_codes import STATUS_CODES
from app.request_objects.course import EnrollmentRequest


class EnrollmentsApi(Resource):
    def __init__(self, unit_of_work: IUnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    def post(self, course_id: str) -> Response:
        params = request.get_json()

        request_object = EnrollmentRequest.from_dict(
            {
                'course_id': course_id,
                'user_id': params['user_id']
            }
        )

        command = enroll_user.EnrollUserCommand(unit_of_work=self.unit_of_work)

        response = command.execute(request=request_object)

        return Response(
            response.serialize(),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )
