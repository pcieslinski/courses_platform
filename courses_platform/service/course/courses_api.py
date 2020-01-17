import json
from flask import Response, request
from flask_restful import Resource

from courses_platform.application.course.commands import create
from courses_platform.application.course.queries import get_all
from courses_platform.application.interfaces.icourse_repository import CRepository

from courses_platform.service.status_codes import STATUS_CODES
from courses_platform.request_objects.course import CreateCourseRequest
from courses_platform.serializers.json_course_serializer import CourseJsonEncoder


class CoursesApi(Resource):
    def __init__(self, repo: CRepository) -> None:
        self.repo = repo

    def get(self) -> Response:
        query = get_all.GetAllCoursesQuery(repo=self.repo)

        response = query.execute()

        return Response(
            json.dumps(response.value, cls=CourseJsonEncoder),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )

    def post(self) -> Response:
        request_object = CreateCourseRequest.from_dict(request.get_json())

        command = create.CreateCourseCommand(repo=self.repo)

        response = command.execute(request=request_object)

        return Response(
            json.dumps(response.value, cls=CourseJsonEncoder),
            mimetype='application/json',
            status=STATUS_CODES[response.type]
        )
