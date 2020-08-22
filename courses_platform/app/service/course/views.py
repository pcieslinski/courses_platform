from typing import List

from flask import Response
from marshmallow import fields
from flask_restful import Resource

from app.service.parser import use_kwargs
from app.application.course import queries
from app.application.course import commands
from app.service.schemas import query_serializer
from app.service.status_codes import STATUS_CODES
from app.application.interfaces.iunit_of_work import IUnitOfWork
from app.service.course.serializers import CourseSchema, course_serializer


class CoursesApi(Resource):
    def __init__(self, unit_of_work: IUnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    @use_kwargs(query_serializer, location='querystring')
    def get(self, include: List[str] = None) -> Response:
        courses_serializer = CourseSchema(many=True, include=include)

        query = queries.GetAllCoursesQuery(unit_of_work=self.unit_of_work)

        response = query.execute()

        return Response(
            response.serialize(courses_serializer),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )

    @use_kwargs(course_serializer)
    def post(self, name: str) -> Response:
        command = commands.CreateCourseCommand(unit_of_work=self.unit_of_work)

        response = command.execute(name=name)

        return Response(
            response.serialize(course_serializer),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )


class CoursesDetailApi(Resource):
    def __init__(self, unit_of_work: IUnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    @use_kwargs(query_serializer, location='querystring')
    def get(self, course_id: str, include: List[str] = None) -> Response:
        course_serializer = CourseSchema(include=include)

        query = queries.GetCourseQuery(unit_of_work=self.unit_of_work)

        response = query.execute(course_id=course_id)

        return Response(
            response.serialize(course_serializer),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )

    def delete(self, course_id: str) -> Response:
        command = commands.DeleteCourseCommand(unit_of_work=self.unit_of_work)

        response = command.execute(course_id=course_id)

        return Response(
            response.serialize(),
            status=STATUS_CODES[response.type]
        )


class EnrollmentsApi(Resource):
    def __init__(self, unit_of_work: IUnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    @use_kwargs({'user_id': fields.Str()})
    def post(self, course_id: str, user_id: str) -> Response:
        command = commands.EnrollUserCommand(unit_of_work=self.unit_of_work)

        response = command.execute(course_id=course_id, user_id=user_id)

        return Response(
            response.serialize(),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )


class EnrollmentsDetailApi(Resource):
    def __init__(self, unit_of_work: IUnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    def delete(self, course_id: str, user_id: str) -> Response:
        command = commands.WithdrawUserEnrollmentCommand(unit_of_work=self.unit_of_work)

        response = command.execute(course_id=course_id, user_id=user_id)

        return Response(
            response.serialize(),
            status=STATUS_CODES[response.type]
        )
