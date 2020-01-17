import json
from flask import Response
from flask_restful import Resource

from courses_platform.application.course.commands import delete
from courses_platform.application.interfaces.icourse_repository import CRepository

from courses_platform.service.status_codes import STATUS_CODES
from courses_platform.request_objects.course import DeleteCourseRequest


class CoursesDetailApi(Resource):
    def __init__(self, repo: CRepository) -> None:
        self.repo = repo

    def delete(self, course_id) -> Response:
        request_object = DeleteCourseRequest.from_dict(dict(course_id=course_id))

        command = delete.DeleteCourseCommand(repo=self.repo)

        response = command.execute(request=request_object)

        return Response(
            json.dumps(response.value),
            status=STATUS_CODES[response.type]
        )
