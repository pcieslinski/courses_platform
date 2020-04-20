import json
from typing import Dict

from app.domain.course import Course


class CourseJsonEncoder(json.JSONEncoder):
    def default(self, course: Course) -> Dict:
        try:
            to_serialize = {
                'id': course.id,
                'name': course.name
            }
            return to_serialize
        except AttributeError:
            return super().default(course)
