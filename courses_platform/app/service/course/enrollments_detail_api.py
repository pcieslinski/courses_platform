from flask import Response
from flask_restful import Resource

from app.service.status_codes import STATUS_CODES
from app.application.interfaces.iunit_of_work import IUnitOfWork
from app.application.course.commands import withdraw_user_enrollment as withdraw


class EnrollmentsDetailApi(Resource):
    def __init__(self, unit_of_work: IUnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    def delete(self, course_id: str, user_id: str) -> Response:
        command = withdraw.WithdrawUserEnrollmentCommand(unit_of_work=self.unit_of_work)

        response = command.execute(course_id=course_id, user_id=user_id)

        return Response(
            response.serialize(),
            status=STATUS_CODES[response.type]
        )
