from typing import List

from flask import Response
from flask_restful import Resource

from app.service.parser import use_kwargs
from app.service.status_codes import STATUS_CODES
from app.service.serializers.schemas import CourseSchema
from app.application.course.queries import GetAllCoursesQuery
from app.application.course.commands import CreateCourseCommand
from app.application.interfaces.iunit_of_work import IUnitOfWork
from app.service.serializers import course_serializer, query_serializer


class CoursesApi(Resource):
    def __init__(self, unit_of_work: IUnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    @use_kwargs(query_serializer, location='querystring')
    def get(self, include: List[str] = None) -> Response:
        courses_serializer = CourseSchema(many=True, include=include)

        query = GetAllCoursesQuery(unit_of_work=self.unit_of_work)

        response = query.execute()

        return Response(
            response.serialize(courses_serializer),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )

    @use_kwargs(course_serializer)
    def post(self, name: str) -> Response:
        command = CreateCourseCommand(unit_of_work=self.unit_of_work)

        response = command.execute(name=name)

        return Response(
            response.serialize(course_serializer),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )
