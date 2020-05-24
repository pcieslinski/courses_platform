from typing import List

from flask import Response
from flask_restful import Resource

from app.service.parser import use_kwargs
from app.application.course.queries import get
from app.service.status_codes import STATUS_CODES
from app.application.course.commands import delete
from app.service.serializers import query_serializer
from app.service.serializers.schemas import CourseSchema
from app.application.interfaces.iunit_of_work import IUnitOfWork


class CoursesDetailApi(Resource):
    def __init__(self, unit_of_work: IUnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    @use_kwargs(query_serializer, location='querystring')
    def get(self, course_id: str, include: List[str] = None) -> Response:
        course_serializer = CourseSchema(include=include)

        query = get.GetCourseQuery(unit_of_work=self.unit_of_work)

        response = query.execute(course_id=course_id)

        return Response(
            response.serialize(course_serializer),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )

    def delete(self, course_id: str) -> Response:
        command = delete.DeleteCourseCommand(unit_of_work=self.unit_of_work)

        response = command.execute(course_id=course_id)

        return Response(
            response.serialize(),
            status=STATUS_CODES[response.type]
        )
