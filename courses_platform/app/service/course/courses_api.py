import json
from flask import Response, request
from flask_restful import Resource

from app.application.course.commands import create
from app.application.course.queries import get_all
from app.application.interfaces.iunit_of_work import IUnitOfWork

from app.serializers import CourseJsonEncoder
from app.service.status_codes import STATUS_CODES
from app.request_objects.course import CreateCourseRequest, GetAllCoursesRequest


class CoursesApi(Resource):
    def __init__(self, unit_of_work: IUnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    def get(self) -> Response:
        request_object = GetAllCoursesRequest.from_dict(dict(request.args))

        query = get_all.GetAllCoursesQuery(unit_of_work=self.unit_of_work)

        response = query.execute(request=request_object)

        return Response(
            json.dumps(response.value, cls=CourseJsonEncoder),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )

    def post(self) -> Response:
        request_object = CreateCourseRequest.from_dict(request.get_json())

        command = create.CreateCourseCommand(unit_of_work=self.unit_of_work)

        response = command.execute(request=request_object)

        return Response(
            json.dumps(response.value, cls=CourseJsonEncoder),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )
