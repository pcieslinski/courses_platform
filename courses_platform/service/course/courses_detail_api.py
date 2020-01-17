import json
from flask import Response
from flask_restful import Resource

from courses_platform.application.course.commands import delete
from courses_platform.application.interfaces.icourse_repository import CRepository


class CoursesDetailApi(Resource):
    def __init__(self, repo: CRepository) -> None:
        self.repo = repo

    def delete(self, course_id) -> Response:
        command = delete.DeleteCourseCommand(repo=self.repo)

        try:
            command.execute(course_id)

        except Exception:
            return Response(
                json.dumps({
                    'message': f'No Course has been found for a given id: {course_id}'
                }),
                mimetype='application/json',
                status=404
            )

        return Response(
            json.dumps(''),
            status=204
        )
