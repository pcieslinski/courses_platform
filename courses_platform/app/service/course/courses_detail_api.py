import json
from flask import Response
from flask_restful import Resource

from app.application.course.queries import get
from app.application.course.commands import delete
from app.application.interfaces.idb_session import DbSession

from app.serializers import CourseJsonEncoder
from app.service.status_codes import STATUS_CODES
from app.request_objects.course import DeleteCourseRequest, GetCourseRequest


class CoursesDetailApi(Resource):
    def __init__(self, db_session: DbSession) -> None:
        self.db_session = db_session

    def get(self, course_id: str) -> Response:
        request_object = GetCourseRequest.from_dict(dict(course_id=course_id))

        query = get.GetCourseQuery(db_session=self.db_session)

        response = query.execute(request=request_object)

        return Response(
            json.dumps(response.value, cls=CourseJsonEncoder),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )

    def delete(self, course_id) -> Response:
        request_object = DeleteCourseRequest.from_dict(dict(course_id=course_id))

        command = delete.DeleteCourseCommand(db_session=self.db_session)

        response = command.execute(request=request_object)

        return Response(
            json.dumps(response.value),
            status=STATUS_CODES[response.type]
        )
