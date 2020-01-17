import json
from flask import Response, request
from flask_restful import Resource

from courses_platform.application.course.commands import create
from courses_platform.application.course.queries import get_all
from courses_platform.serializers.json_course_serializer import CourseJsonEncoder
from courses_platform.application.interfaces.icourse_repository import CRepository


class CoursesApi(Resource):
    def __init__(self, repo: CRepository) -> None:
        self.repo = repo

    def get(self) -> Response:
        query = get_all.GetAllCoursesQuery(repo=self.repo)

        result = query.execute()

        return Response(
            json.dumps(result, cls=CourseJsonEncoder),
            mimetype='application/json',
            status=200
        )

    def post(self) -> Response:
        req_data = request.get_json()

        command = create.CreateCourseCommand(repo=self.repo)

        result = command.execute(req_data['name'])

        return Response(
            json.dumps(result, cls=CourseJsonEncoder),
            mimetype='application/json',
            status=201
        )
