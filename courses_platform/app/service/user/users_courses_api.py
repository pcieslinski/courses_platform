from flask import Response
from flask_restful import Resource

from app.application.user.queries import get_user_courses
from app.application.interfaces.iunit_of_work import IUnitOfWork

from app.serializers import courses_serializer
from app.service.status_codes import STATUS_CODES
from app.request_objects.user import GetUserRequest


class UsersCoursesApi(Resource):
    def __init__(self, unit_of_work: IUnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    def get(self, user_id: str) -> Response:
        request_object = GetUserRequest.from_dict(dict(user_id=user_id))

        query = get_user_courses.GetUserCoursesQuery(unit_of_work=self.unit_of_work)

        response = query.execute(request=request_object)

        return Response(
            response.serialize(courses_serializer),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )
