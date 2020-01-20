import json
from flask import Response
from flask_restful import Resource

from courses_platform.application.user.queries import get_user_courses
from courses_platform.application.interfaces.idb_session import DbSession

from courses_platform.service.status_codes import STATUS_CODES
from courses_platform.request_objects.user import GetUserRequest
from courses_platform.serializers.json_course_serializer import CourseJsonEncoder


class UsersCoursesApi(Resource):
    def __init__(self, db_session: DbSession) -> None:
        self.db_session = db_session

    def get(self, user_id: str) -> Response:
        request_object = GetUserRequest.from_dict(dict(user_id=user_id))

        query = get_user_courses.GetUserCoursesQuery(db_session=self.db_session)

        response = query.execute(request=request_object)

        return Response(
            json.dumps(response.value, cls=CourseJsonEncoder),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )
