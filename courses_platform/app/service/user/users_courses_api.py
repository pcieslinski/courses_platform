from flask import Response
from flask_restful import Resource

from app.serializers import courses_serializer
from app.service.status_codes import STATUS_CODES
from app.application.user.queries import get_user_courses
from app.application.interfaces.iunit_of_work import IUnitOfWork


class UsersCoursesApi(Resource):
    def __init__(self, unit_of_work: IUnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    def get(self, user_id: str) -> Response:
        query = get_user_courses.GetUserCoursesQuery(unit_of_work=self.unit_of_work)

        response = query.execute(user_id=user_id)

        return Response(
            response.serialize(courses_serializer),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )
