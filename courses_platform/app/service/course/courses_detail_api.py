from flask import Response
from flask_restful import Resource

from app.application.course.queries import get
from app.application.course.commands import delete
from app.application.interfaces.iunit_of_work import IUnitOfWork

from app.serializers import course_serializer
from app.service.status_codes import STATUS_CODES
from app.request_objects.course import DeleteCourseRequest, GetCourseRequest


class CoursesDetailApi(Resource):
    def __init__(self, unit_of_work: IUnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    def get(self, course_id: str) -> Response:
        request_object = GetCourseRequest.from_dict(dict(course_id=course_id))

        query = get.GetCourseQuery(unit_of_work=self.unit_of_work)

        response = query.execute(request=request_object)

        return Response(
            response.serialize(course_serializer),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )

    def delete(self, course_id: str) -> Response:
        request_object = DeleteCourseRequest.from_dict(dict(course_id=course_id))

        command = delete.DeleteCourseCommand(unit_of_work=self.unit_of_work)

        response = command.execute(request=request_object)

        return Response(
            response.serialize(),
            status=STATUS_CODES[response.type]
        )
