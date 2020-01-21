import json
from uuid import uuid4
from typing import Tuple

from app.serializers import json_course_serializer as ser


def create_stub_course() -> Tuple[object, str]:
    course_id = str(uuid4())

    class StubCourse:
        def __init__(self):
            self.id = course_id
            self.name = 'Test Course'

    return StubCourse(), course_id


def test_serialize_user_entity():
    course, course_id = create_stub_course()
    course_json = json.dumps(course, cls=ser.CourseJsonEncoder)

    expected = f'''
        {{"id": "{course_id}",
        "name": "Test Course"}}
    '''

    assert json.loads(course_json) == json.loads(expected)
