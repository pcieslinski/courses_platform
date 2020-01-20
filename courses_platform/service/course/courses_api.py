import json
from flask import Response, request
from flask_restful import Resource

from courses_platform.application.course.commands import create
from courses_platform.application.course.queries import get_all
from courses_platform.application.interfaces.idb_session import DbSession

from courses_platform.service.status_codes import STATUS_CODES
from app.serializers.json_course_serializer import CourseJsonEncoder
from courses_platform.request_objects.course import CreateCourseRequest, GetAllCoursesRequest


class CoursesApi(Resource):
    def __init__(self, db_session: DbSession) -> None:
        self.db_session = db_session

    def get(self) -> Response:
        request_object = GetAllCoursesRequest.from_dict(dict(request.args))

        query = get_all.GetAllCoursesQuery(db_session=self.db_session)

        response = query.execute(request=request_object)

        return Response(
            json.dumps(response.value, default=lambda o: o.__dict__),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )

    def post(self) -> Response:
        request_object = CreateCourseRequest.from_dict(request.get_json())

        command = create.CreateCourseCommand(db_session=self.db_session)

        response = command.execute(request=request_object)

        return Response(
            json.dumps(response.value, cls=CourseJsonEncoder),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )
