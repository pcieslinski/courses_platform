from flask import Response
from marshmallow import fields
from flask_restful import Resource

from app.service.parser import use_kwargs
from app.service.status_codes import STATUS_CODES
from app.application.course.commands import enroll_user
from app.application.interfaces.iunit_of_work import IUnitOfWork


class EnrollmentsApi(Resource):
    def __init__(self, unit_of_work: IUnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    @use_kwargs({'user_id': fields.Str()})
    def post(self, course_id: str, user_id: str) -> Response:
        command = enroll_user.EnrollUserCommand(unit_of_work=self.unit_of_work)

        response = command.execute(course_id=course_id, user_id=user_id)

        return Response(
            response.serialize(),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )
